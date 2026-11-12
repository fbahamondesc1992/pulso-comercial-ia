"""Audita índice y objetos Git sin mostrar coincidencias ni credenciales."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dotenv import dotenv_values
from scripts.preparar_entrega import recopilar, verificar_contenidos


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def auditar():
    key = dotenv_values(ROOT / '.env', interpolate=False).get('OPENAI_API_KEY')
    permitidos = set(recopilar(ROOT))
    index = {}
    for line in git('ls-files', '--stage', '-z').split(b'\0'):
        if not line:
            continue
        meta, name = line.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        path = name.decode()
        if path not in permitidos or mode not in ('100644', '100755') or stage != '0':
            raise ValueError('Ruta, modo o conflicto no permitido en el índice Git.')
        index[path] = git('cat-file', 'blob', oid)
    if not index:
        raise ValueError('Índice vacío; no certifica una publicación.')
    verificar_contenidos(index, key)
    # Incluye objetos alcanzables y huérfanos, mensajes de commits y blobs históricos.
    objects = git('cat-file', '--batch-all-objects', '--batch-check=%(objectname) %(objecttype)').decode().splitlines()
    for row in objects:
        oid, kind = row.split()
        verificar_contenidos({f'objeto_git/{oid}/{kind}': git('cat-file', kind, oid)}, key)
        if kind == 'tree':
            for item in git('ls-tree', '-rz', oid).split(b'\0'):
                if not item:
                    continue
                meta, name = item.split(b'\t', 1)
                path = Path(name.decode())
                if any(part.startswith('.env') and part != '.env.example' for part in path.parts):
                    raise ValueError('Archivo de entorno presente en historial Git.')
                if meta.startswith(b'120000') or meta.startswith(b'160000'):
                    raise ValueError('Enlace o submódulo no permitido en historial.')
    head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
    return {'fecha_utc': datetime.now(timezone.utc).isoformat(),
            'head': head.stdout.strip() if head.returncode == 0 else None,
            'archivos_indice': len(index), 'objetos_git_inspeccionados': len(objects),
            'hallazgos': 0, 'alcance': 'Índice por lista explícita; todos los objetos Git, incluidos huérfanos.',
            'limitacion': 'Patrones y coincidencia de clave local; no garantía universal.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', required=True)
    args = parser.parse_args()
    out = Path(args.salida)
    if out.exists():
        parser.error('La evidencia ya existe; usar otro archivo.')
    result = auditar()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))
