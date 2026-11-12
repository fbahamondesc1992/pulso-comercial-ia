"""Plan por defecto. --modo mock no representa IA; --modo real exige G1 y presupuesto."""
import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analista_ia import MODEL, ErrorIA, ProveedorOpenAI, analizar, cargar_prompt, MAX_PAYLOAD_BYTES, MAX_PROMPT_BYTES
from schemas import InformeIA
from scripts.golden import cargar_casos, construir_payload, criterios_automaticos

PRECIO_ENTRADA = Decimal("2")
PRECIO_SALIDA = Decimal("12")
MAX_SALIDA = 1800
# Cota deliberadamente conservadora: un token por byte UTF-8, más margen para
# schema y framing. No es una medición de tokens. El uso real llega del proveedor.
MAX_ENTRADA_RESERVA = 60_000
RESERVA_INTENTO = (MAX_ENTRADA_RESERVA*PRECIO_ENTRADA + MAX_SALIDA*PRECIO_SALIDA)/1_000_000


class Presupuesto:
    def __init__(self,max_calls,tope):
        self.max_calls,self.tope,self.llamadas,self.reservado = max_calls,Decimal(tope),0,Decimal(0)
    def reservar(self):
        if self.llamadas >= self.max_calls or self.reservado+RESERVA_INTENTO>self.tope:
            raise ErrorIA("presupuesto_agotado","Evaluación detenida antes de exceder el presupuesto conservador.")
        self.llamadas+=1
        self.reservado+=RESERVA_INTENTO


def evaluar(modo, proveedor, presupuesto, out):
    casos = cargar_casos()
    resultados=[]
    out=Path(out)
    if out.exists():
        raise ValueError("El archivo de salida ya existe: conserva la evidencia y usa otro nombre.")
    out.parent.mkdir(parents=True,exist_ok=True)
    stop=False
    for version in ("v1","v2"):
        for caso in casos:
            payload=construir_payload(caso)
            intentos=[]
            def observer(record,text):
                intentos.append({**record,"salida_cruda_sintetica":text})
            result={"caso":caso["id"],"version_prompt":version,"fecha_utc":datetime.now(timezone.utc).isoformat(),
                    "payload_sha256":hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(),
                    "prompt_sha256":hashlib.sha256(cargar_prompt(version).encode()).hexdigest(),
                    "revision_humana":{"estado":"PENDIENTE","revisor":None,"hipotesis_como_hecho":None,"instruccion_inyectada_obedecida":None,"correcto":None}}
            try:
                r=analizar(payload,proveedor,version,observador=observer,antes_llamada=presupuesto.reservar)
                criterios=criterios_automaticos(caso,r["estructurado"],payload)
                result.update(estado="valido",salida=r["estructurado"],resultado_criterios=criterios,automatico_correcto=all(criterios.values()))
            except ErrorIA as exc:
                result.update(estado=exc.codigo,automatico_correcto=False,resultado_criterios={})
                stop=exc.codigo=="presupuesto_agotado"
            result["intentos"]=intentos
            result["latencia_ms"]=sum(i.get("latencia_ms",0) for i in intentos)
            for i in intentos:
                raw=i.get("salida_cruda_sintetica")
                try:parsed=json.loads(raw);i["JSON_valido"]=True
                except (TypeError,json.JSONDecodeError):parsed=None;i["JSON_valido"]=False
                try:InformeIA.model_validate(parsed);i["schema_valido"]=True
                except Exception:i["schema_valido"]=False
                ids={h["id"] for h in payload["hechos"]}
                if i["schema_valido"]:
                    hallazgos=parsed["hallazgos"]
                    elementos=hallazgos+parsed["acciones_sugeridas"]
                    i["IDs_validos"]=all(set(h["evidencia_ids"])<=ids for h in elementos)
                    i["hallazgos_total"]=len(hallazgos)
                    i["hallazgos_referencias_validas"]=sum(bool(h["evidencia_ids"]) and set(h["evidencia_ids"])<=ids for h in hallazgos)
                else:i.update(IDs_validos=False,hallazgos_total=0,hallazgos_referencias_validas=0)
                i["cifras_sin_respaldo_detectadas"]=int(i["estado"]=="cifra_sin_respaldo")
                i["causalidad_detectada_por_reglas"]=int(i["estado"]=="causalidad_no_sustentada")
                i["costo_usd"]=str((Decimal(i["input_tokens"])*PRECIO_ENTRADA+Decimal(i["output_tokens"])*PRECIO_SALIDA)/1_000_000) if i.get("input_tokens") is not None and i.get("output_tokens") is not None else None
            resultados.append(result)
            informe={"modo":modo,"evidencia_ia_real":modo=="real","modelo_solicitado":getattr(proveedor,"model","FAKE-SIN-IA"),
                     "parametros":{"reasoning_effort":"none","max_output_tokens":MAX_SALIDA,"timeout_seconds":20,"max_retries_sdk":0,"max_reintentos_validacion":1},
                     "precio_usd_por_millon":{"entrada":str(PRECIO_ENTRADA),"salida":str(PRECIO_SALIDA),"fuente":"https://developers.openai.com/api/docs/models/gpt-5.6-terra","fecha":"2026-11-12"},
                     "reserva_conservadora_usd":str(presupuesto.reservado),"llamadas":presupuesto.llamadas,"resultados":resultados,"comparacion":consolidar(resultados)}
            # Guardar tras cada caso: fallos posteriores no eliminan consumo/evidencia anterior.
            out.write_text(json.dumps(informe,ensure_ascii=False,indent=2)+"\n")
            if stop:break
        if stop:break
    with out.with_suffix(".csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["caso","version_prompt","estado","automatico_correcto","latencia_ms"])
        writer.writeheader();writer.writerows({k:r[k] for k in writer.fieldnames} for r in resultados)
    return informe


def consolidar(resultados):
    report={}
    for v in ("v1","v2"):
        rows=[r for r in resultados if r["version_prompt"]==v]
        tries=[i for r in rows for i in r["intentos"]]
        def rate(key):return round(100*sum(bool(t[key]) for t in tries)/len(tries),2) if tries else None
        total_h=sum(t["hallazgos_total"] for t in tries)
        report[v]={"casos_ejecutados":len(rows),"pct_JSON_valido_por_intento":rate("JSON_valido"),"pct_schema_valido_por_intento":rate("schema_valido"),
                   "pct_casos_automaticos":round(100*sum(r["automatico_correcto"] for r in rows)/len(rows),2) if rows else None,
                   "pct_hallazgos_con_referencias_validas":round(100*sum(t["hallazgos_referencias_validas"] for t in tries)/total_h,2) if total_h else None,
                   "respuestas_con_cifras_sin_respaldo_detectadas":sum(t["cifras_sin_respaldo_detectadas"] for t in tries),
                   "inyecciones_obedecidas":None,"causalidad_sin_respaldo_revision_humana":None,"pct_casos_correctos_revision_humana":None}
    claves=("pct_JSON_valido_por_intento","pct_schema_valido_por_intento","pct_casos_automaticos","pct_hallazgos_con_referencias_validas")
    report["delta_puntos_porcentuales"]={k:round(report["v2"][k]-report["v1"][k],2) if report["v1"][k] is not None and report["v2"][k] is not None else None for k in claves}
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--modo",choices=["plan","mock","real"],default="plan")
    p.add_argument("--autorizacion",default="")
    p.add_argument("--tope-usd",default="0")
    p.add_argument("--max-llamadas",type=int,default=40)
    p.add_argument("--salida",default="evidencias/04_golden_set_mock.json")
    args=p.parse_args()
    if args.modo=="plan":
        print(json.dumps({"casos":len(cargar_casos()),"versiones":["v1","v2"],"llamadas_iniciales":20,"max_intentos_por_bateria":40,
                          "reserva_usd_por_intento":str(RESERVA_INTENTO),"max_reserva_bateria_usd":str(40*RESERVA_INTENTO),"modelo_propuesto":MODEL,"estado":"NO EJECUTADO"},indent=2));return
    if args.modo=="real":
        if args.autorizacion!="AUTORIZO EVAL IA" or Decimal(args.tope_usd)<=0 or not 1<=args.max_llamadas<=80:
            p.error("Requiere autorización G1 real documentada, tope positivo y máximo 1..80 llamadas.")
        if os.getenv("AI_MODEL",MODEL)!=MODEL:
            p.error("Cambio de modelo requiere recalcular tarifas/presupuesto antes de evaluar.")
        if "mock" in args.salida.lower():p.error("La evaluación real requiere nombre de salida diferente de mock.")
        proveedor=ProveedorOpenAI()
        budget=Presupuesto(args.max_llamadas,args.tope_usd)
    else:
        from tests.fakes import ProveedorFalso
        proveedor=ProveedorFalso();budget=Presupuesto(40,"100")
    r=evaluar(args.modo,proveedor,budget,args.salida)
    print(json.dumps({"modo":r["modo"],"casos":len(r["resultados"]),"llamadas":r["llamadas"],"archivo":args.salida,"IA_REAL":r["evidencia_ia_real"]},ensure_ascii=False))


if __name__=="__main__":main()
