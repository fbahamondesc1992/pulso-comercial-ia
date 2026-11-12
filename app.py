"""Aplicación sin persistencia: cada petición recalcula el archivo en memoria."""
import io
import json
import os
import threading
import time
from collections import defaultdict, deque
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, Request, jsonify, render_template, request, send_file
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from analista_ia import ErrorIA, ProveedorOpenAI, analizar, resumen_local
from indicadores import calcular, filtros_iniciales, hechos_para_ia
from schemas import Filtros
from validador_csv import ErrorCSV, MAX_BYTES, leer_csv

ROOT = Path(__file__).resolve().parent


class PeticionEnMemoria(Request):
    def _get_file_stream(self, total_content_length, content_type, filename=None, content_length=None):
        return io.BytesIO()


class LimiteDemo:
    """Contador por proceso, NO límite duradero de gasto. Ver docs/COSTOS_Y_LIMITACIONES.md."""
    def __init__(self, por_ip=5, global_hora=30):
        self.por_ip, self.global_hora = por_ip, global_hora
        self.globales, self.ips, self.lock = deque(), defaultdict(deque), threading.Lock()

    def admitir(self, ip):
        ahora = time.monotonic()
        with self.lock:
            while self.globales and self.globales[0] <= ahora - 3600:
                self.globales.popleft()
            for key in list(self.ips):
                q = self.ips[key]
                while q and q[0] <= ahora - 3600:
                    q.popleft()
                if not q:
                    del self.ips[key]
            if len(self.globales) >= self.global_hora or len(self.ips.get(ip, [])) >= self.por_ip:
                return False
            self.globales.append(ahora)
            self.ips[ip].append(ahora)
            return True


def create_app(config=None, proveedor=None):
    app = Flask(__name__)
    app.request_class = PeticionEnMemoria
    app.config.update(MAX_CONTENT_LENGTH=MAX_BYTES + 64 * 1024, MAX_FORM_MEMORY_SIZE=64 * 1024,
                      MAX_FORM_PARTS=10, TESTING=False, JSON_SORT_KEYS=False)
    if config:
        app.config.update(config)
    app.extensions["limite_demo"] = LimiteDemo(int(os.getenv("AI_REQUESTS_PER_IP_HOUR", "5")), int(os.getenv("AI_REQUESTS_GLOBAL_HOUR", "30")))

    @app.before_request
    def proteger_origen():
        if request.path.startswith("/api/"):
            if request.headers.get("X-Pulso-Request") != "1":
                return jsonify(error="Solicitud inválida. Usa los controles del dashboard."), 403
            origin = request.headers.get("Origin")
            if origin and (urlsplit(origin).scheme not in ("http", "https") or urlsplit(origin).netloc != request.host):
                return jsonify(error="Origen de solicitud no permitido."), 403

    @app.after_request
    def headers(response):
        response.headers.update({"Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",
                                 "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
                                 "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
                                 "Cache-Control": "no-store", "X-Frame-Options": "DENY"})
        return response

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok", servicio="pulso-comercial-ia"), 200

    @app.get("/demo.csv")
    def demo():
        return send_file(ROOT / "datos/demo_ventas.csv", as_attachment=True, download_name="demo_ventas.csv", mimetype="text/csv")

    def obtener_resultado():
        if request.form.get("fuente") == "demo":
            contenido = (ROOT / "datos/demo_ventas.csv").read_bytes()
            nombre = "demo_ventas.csv"
        elif request.form.get("fuente") == "archivo" and "archivo" in request.files:
            archivo = request.files["archivo"]
            contenido, nombre = archivo.read(MAX_BYTES + 1), archivo.filename or ""
        else:
            raise ErrorCSV("Selecciona la demo o un archivo CSV ficticio.")
        ds = leer_csv(contenido, nombre)
        raw = request.form.get("filtros")
        filters = Filtros.model_validate_json(raw) if raw else filtros_iniciales(ds)
        return calcular(ds, filters)

    @app.post("/api/dashboard")
    def dashboard():
        resultado = obtener_resultado()
        payload, aliases = hechos_para_ia(resultado)
        resultado["hechos"], resultado["etiquetas"] = payload["hechos"], aliases
        return jsonify(resultado)

    @app.post("/api/analisis")
    def informe():
        resultado = obtener_resultado()
        if request.form.get("snapshot") != resultado["snapshot"]:
            return jsonify(error="Los filtros o datos cambiaron. Actualiza el dashboard antes de generar el análisis."), 409
        payload, aliases = hechos_para_ia(resultado)
        try:
            client = proveedor or ProveedorOpenAI(timeout=float(os.getenv("AI_TIMEOUT_SECONDS", "20")), max_output_tokens=int(os.getenv("AI_MAX_OUTPUT_TOKENS", "1800")))
            # remote_addr sin confiar en X-Forwarded-For arbitrario. En proxy puede agrupar visitantes.
            if not app.extensions["limite_demo"].admitir(request.remote_addr or "desconocida"):
                return jsonify(error="Se alcanzó el cupo temporal de la demo. Puedes seguir explorando los indicadores.", respaldo=resumen_local(resultado)), 429
            result = analizar(payload, client, version=os.getenv("ANALYST_PROMPT_VERSION", "v2"))
            result.update(snapshot=resultado["snapshot"], hechos=payload["hechos"], etiquetas=aliases)
            # No devolver intento/respuesta cruda ni request_id del proveedor en la interfaz.
            result.pop("estructurado", None)
            result["metadatos"] = {k: result["metadatos"][k] for k in ("prompt", "modelo")}
            return jsonify(result)
        except ErrorIA as exc:
            return jsonify(error=str(exc), codigo=exc.codigo, respaldo=resumen_local(resultado)), 503 if exc.codigo in ("sin_clave", "ia_deshabilitada") else 502

    @app.errorhandler(ErrorCSV)
    @app.errorhandler(ValueError)
    def dato_invalido(error):
        if isinstance(error, ValidationError):
            mensaje = "Filtros inválidos: revisa años, meses, dimensiones y campos permitidos."
        elif isinstance(error, ErrorCSV):
            mensaje = str(error)
        else:
            # Solo ValueError del motor: texto fijo, nunca el valor recibido.
            mensaje = str(error) if str(error) in {
                "No se pueden analizar meses futuros.", "El año actual no existe en el archivo.",
                "No hay datos para el período y los filtros seleccionados.", "El archivo solo contiene años futuros.",
                "No hay meses actuales calculables."} else "Parámetros inválidos. Revisa el período y los filtros."
        return jsonify(error=mensaje), 400

    @app.errorhandler(HTTPException)
    def error_http(error):
        mensaje = "El archivo supera el tamaño permitido de la demo." if error.code == 413 else "Solicitud no disponible. Revisa la ruta y vuelve a intentar."
        return jsonify(error=mensaje), error.code

    @app.errorhandler(Exception)
    def error_interno(error):
        app.logger.error("Fallo interno controlado: %s", type(error).__name__)
        return jsonify(error="No se pudo completar la solicitud. Intenta nuevamente."), 500

    return app


if __name__ == "__main__":
    from dotenv import load_dotenv
    # Solo arranque local explícito. Importar la app en pytest o Gunicorn NO lee .env.
    load_dotenv(ROOT / ".env", override=False, interpolate=False)

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "8080")), debug=False)
