"""Revalida salidas sintéticas existentes sin proveedor, sin red y sin regenerarlas."""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analista_ia import ErrorIA, validar_informe, cargar_prompt, VALIDADOR_VERSION
from scripts.golden import cargar_casos, construir_payload, criterios_automaticos, CRITERIOS_VERSION

REVALIDACION_VERSION = "2"
ESTADOS_REVALIDABLES = {
    'valido', 'json_invalido', 'schema_invalido', 'ids_invalidos',
    'requiere_abstencion', 'hallazgo_sin_evidencia', 'cifra_sin_respaldo',
    'contenido_externo', 'causalidad_no_sustentada',
}


def sha(content):
    return hashlib.sha256(content).hexdigest()


def revalidar(origen):
    path = Path(origen)
    original = path.read_bytes()
    data = json.loads(original)
    casos = {c['id']: c for c in cargar_casos()}
    resultados = []
    for caso in data['resultados']:
        fixture = casos[caso['caso']]
        payload = construir_payload(fixture)
        if sha(json.dumps(payload, sort_keys=True).encode()) != caso['payload_sha256']:
            raise ValueError('El payload cambió; no se puede comparar con esta evidencia.')
        if sha(cargar_prompt(caso['version_prompt']).encode()) != caso['prompt_sha256']:
            raise ValueError('El prompt cambió; esta revalidación requiere conservarlo.')
        intentos = []
        for intento in caso['intentos']:
            raw = intento.get('salida_cruda_sintetica')
            result = {'intento': intento['intento'], 'estado_original': intento['estado'],
                      'salida_sha256': sha(raw.encode()) if isinstance(raw, str) else None}
            if intento['estado'] not in ESTADOS_REVALIDABLES:
                # JSON completo no prueba que el proveedor haya terminado correctamente.
                result.update(estado_revalidado=intento['estado'], criterios={}, automatico_correcto=False,
                              motivo='Estado operativo no revalidable; no se convierte en respuesta válida.')
                intentos.append(result)
                continue
            try:
                informe = validar_informe(raw, payload)
                criterios = criterios_automaticos(fixture, informe.model_dump(), payload)
                result.update(estado_revalidado='valido', criterios=criterios,
                              automatico_correcto=all(criterios.values()))
            except ErrorIA as exc:
                result.update(estado_revalidado=exc.codigo, criterios={}, automatico_correcto=False)
            intentos.append(result)
        # Respuestas ya observadas; no se proyecta lo que habría generado otro intento.
        primero = next((i for i in intentos if i['estado_revalidado'] == 'valido'), None)
        resultados.append({'caso': caso['caso'], 'prompt': caso['version_prompt'],
                           'automatico_original': caso['automatico_correcto'], 'intentos': intentos,
                           'primer_intento_observado_aceptado': primero['intento'] if primero else None,
                           'automatico_revalidado': primero['automatico_correcto'] if primero else False})
    resumen = {}
    for version in ('v1', 'v2'):
        rows = [r for r in resultados if r['prompt'] == version]
        resumen[version] = {'casos': len(rows),
                            'cumplen_original': sum(r['automatico_original'] for r in rows),
                            'cumplen_revalidacion': sum(r['automatico_revalidado'] for r in rows)}
    if path.read_bytes() != original:
        raise ValueError('La evidencia cambió durante la revisión.')
    return {'fecha_utc': datetime.now(timezone.utc).isoformat(),
            'tipo': 'REVALIDACION_OFFLINE_DE_RESPUESTAS_EXISTENTES',
            'llamadas_api': 0, 'costo_nuevo_usd': '0', 'revision_humana': 'PENDIENTE',
            'no_demuestra_mejora_del_prompt': True,
            'evidencia_original': path.name, 'sha256_original': sha(original),
            'validador_version': VALIDADOR_VERSION, 'criterios_version': CRITERIOS_VERSION,
            'revalidacion_version': REVALIDACION_VERSION,
            'sha256_archivos': {p: sha((ROOT / p).read_bytes()) for p in (
                'analista_ia.py', 'scripts/golden.py', 'prompts/analista_v1.md',
                'prompts/analista_v2.md', 'golden_set/casos_analista.json')},
            'resumen': resumen, 'resultados': resultados}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origen', default='evidencias/13_evaluacion_real.json')
    parser.add_argument('--salida', default='evidencias/14_revalidacion_offline.json')
    args = parser.parse_args()
    target = Path(args.salida)
    if target.exists():
        parser.error('No se sobrescriben evidencias existentes.')
    report = revalidar(args.origen)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('tipo', 'llamadas_api', 'resumen')}, ensure_ascii=False))
