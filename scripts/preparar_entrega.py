"""Prepara un ZIP local por lista explícita; no inicializa Git ni publica recursos."""
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.auditar_secretos import PATRONES

ARCHIVOS_RAIZ = {
    "PROMPT_MAESTRO.md", "AGENTS.md", "README.md", "app.py", "validador_csv.py",
    "indicadores.py", "analista_ia.py", "schemas.py", "requirements.txt",
    "requirements-dev.txt", "Dockerfile", ".dockerignore", ".gitignore", ".gitattributes", ".env.example", "pytest.ini",
}
DIRECTORIOS = {"templates", "static", "datos", "prompts", "golden_set", "scripts", "tests", "docs", "evidencias"}
OMITIR = {"__pycache__", ".pytest_cache", ".git", ".venv", "node_modules"}


def recopilar(root=ROOT):
    root = Path(root)
    paths = [root / name for name in sorted(ARCHIVOS_RAIZ)]
    for folder in sorted(DIRECTORIOS):
        base = root / folder
        if base.is_symlink():
            raise ValueError("No se empaquetan directorios enlazados.")
        paths.extend(p for p in base.rglob("*") if p.is_file() and not any(part in OMITIR for part in p.relative_to(root).parts)
                     and p.suffix not in (".pyc", ".pyo") and p.name != ".DS_Store")
    archivos = {}
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or path.is_symlink() or root.resolve() not in path.resolve().parents:
            raise ValueError(f"Archivo requerido ausente o enlace no permitido: {relative}")
        if any(part.startswith(".env") and part != ".env.example" for part in path.relative_to(root).parts):
            raise ValueError("Se encontró un archivo de entorno en el contenido publicable.")
        archivos[relative] = path.read_bytes()
    return archivos


def verificar_contenidos(archivos, secreto_local=None):
    hallazgos = []
    for path, content in archivos.items():
        if secreto_local and secreto_local.encode() in content:
            hallazgos.append({"archivo": path, "tipo": "coincidencia_credencial_local"})
        text = content.decode("utf-8", errors="ignore")
        for tipo, pattern in PATRONES.items():
            if pattern.search(text):
                hallazgos.append({"archivo": path, "tipo": tipo})
    if hallazgos:
        # Solo archivos/tipos; nunca contenido ni coincidencias.
        raise ValueError("Contenido no publicable: " + json.dumps(hallazgos, ensure_ascii=False))


def preparar(root=ROOT):
    root = Path(root)
    from dotenv import dotenv_values
    key = dotenv_values(root / ".env", interpolate=False).get("OPENAI_API_KEY") if (root / ".env").exists() else None
    files = recopilar(root)
    verificar_contenidos(files, key)
    manifest = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "estado": "MVP_LOCAL_NO_PUBLICADO",
                "sin_credenciales": True, "git_creado": False, "despliegue_realizado": False,
                "limitacion_auditoria": "Patrones y coincidencia exacta de credencial local; no garantía exhaustiva.",
                "archivos": [{"ruta": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()} for name, content in files.items()]}
    folder = root / "entrega"
    folder.mkdir(exist_ok=True)
    target = folder / "Pulso_Comercial_IA_MVP_LOCAL.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for name, content in files.items():
            z.writestr("pulso-comercial-ia/" + name, content)
        z.writestr("pulso-comercial-ia/MANIFIESTO_ENTREGA.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        empaquetados = {name: z.read(name) for name in z.namelist()}
        verificar_contenidos(empaquetados, key)
        assert all(not name.endswith("/.env") for name in z.namelist())
    report = {"archivo": str(target.relative_to(root)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
              "archivos_fuente": len(files), "bytes_zip": target.stat().st_size,
              "estado": manifest["estado"], "secretos_detectados": 0, "exclusiones": [".env", ".venv", ".git", "caches", "PDF original del curso", "entrega/"]}
    (folder / "VERIFICACION_PAQUETE.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))
    return target


if __name__ == "__main__":
    preparar()
