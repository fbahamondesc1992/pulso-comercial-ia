"""Inspección local por patrones; no imprime coincidencias ni valores secretos."""
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXCLUIR={'.venv','.git','__pycache__','.pytest_cache','tmp','node_modules'}
BINARIOS={'.png','.jpg','.jpeg','.pdf','.pyc','.zip'}
PATRONES={
    'clave_openai':re.compile(r'\bsk-[A-Za-z0-9_-]{24,}'),
    'token_github':re.compile(r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{30,}'),
    'clave_aws':re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'clave_privada':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'asignacion_api_key':re.compile(r'(?m)^OPENAI_API_KEY[ \t]*=[ \t]*["\x27]?[A-Za-z0-9_-]{15,}'),
}


def auditar():
    hallazgos=[];files=[]
    for path in sorted(ROOT.rglob('*')):
        relative=path.relative_to(ROOT)
        if any(p in EXCLUIR for p in relative.parts) or not path.is_file() or path.suffix in BINARIOS:
            continue
        if relative.as_posix()=='evidencias/05_secretos_local.json':continue
        if path.name=='.env' or (path.name.startswith('.env.') and path.name!='.env.example'):
            hallazgos.append({'archivo':str(relative),'tipo':'archivo_entorno_no_publicable'})
        try:content=path.read_text(encoding='utf-8')
        except UnicodeDecodeError:continue
        files.append({'archivo':str(relative),'sha256':hashlib.sha256(content.encode()).hexdigest()})
        for name,pattern in PATRONES.items():
            if pattern.search(content):hallazgos.append({'archivo':str(relative),'tipo':name})
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'metodo':'patrones + exclusiones; sin valores en salida',
            'historial_git':'NO EXISTE; revisar nuevamente antes de G2','archivos_texto_inspeccionados':len(files),
            'hallazgos':hallazgos,'inventario':files,'limitacion':'No sustituye un escáner exhaustivo; binarios no inspeccionados por estos patrones.'}
    (ROOT/'evidencias/05_secretos_local.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('archivos_texto_inspeccionados','hallazgos','historial_git')},ensure_ascii=False))
    return bool(hallazgos)


if __name__=='__main__':raise SystemExit(auditar())
