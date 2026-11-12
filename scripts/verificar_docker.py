"""Lee únicamente el contenedor local de esta tarea y sus endpoints sin IA real."""
import json
import argparse
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida',default='evidencias/03_docker_verificacion.json')
    args=parser.parse_args()
    container=json.loads(subprocess.check_output(['docker','inspect','pulso-local-g0']))[0]
    image=json.loads(subprocess.check_output(['docker','image','inspect',container['Image']]))[0]
    env=container['Config']['Env']
    assert 'AI_ENABLED=false' in env
    assert not any(v.startswith('OPENAI_API_KEY=') and len(v)>len('OPENAI_API_KEY=') for v in env)
    assert container['Config']['User']=='10001'
    assert image['Architecture']=='amd64'
    with urllib.request.urlopen('http://127.0.0.1:8081/health',timeout=5) as r:
        status=r.status;health=json.load(r)
    def post(path,data):
        req=urllib.request.Request('http://127.0.0.1:8081'+path,data=urllib.parse.urlencode(data).encode(),headers={'X-Pulso-Request':'1'})
        with urllib.request.urlopen(req,timeout=10) as r:return r.status,json.load(r)
    dash_status,dash=post('/api/dashboard',{'fuente':'demo'})
    assert dash['total']['real']['valor']=='471435750'
    assert dash['total']['brecha']['valor']=='-30044250'
    # Comprobar el fallo esperado de IA deshabilitada sin consumir proveedor.
    try:post('/api/analisis',{'fuente':'demo','snapshot':dash['snapshot']})
    except urllib.error.HTTPError as error:
        ai_status=error.code;ai=json.load(error)
    else:raise AssertionError('La IA debía estar deshabilitada')
    assert ai_status==503 and ai['codigo']=='ia_deshabilitada'
    files=subprocess.check_output(['docker','exec','pulso-local-g0','python','-c',
        "from pathlib import Path; print('\\n'.join(str(p) for p in Path('/app').rglob('*') if p.is_file()))"],text=True).splitlines()
    assert not any('/.env' in p or '/tests/' in p or '/evidencias/' in p or '/.git/' in p for p in files)
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'contenedor':'pulso-local-g0','image_id':container['Image'],
            'architecture':image['Architecture'],'usuario':container['Config']['User'],'ai_enabled':False,'api_key_en_imagen':False,
            'health_http':status,'health':health,'dashboard_http':dash_status,'real_demo_clp':dash['total']['real']['valor'],
            'brecha_demo_clp':dash['total']['brecha']['valor'],'ia_http':ai_status,'ia_codigo':ai['codigo'],
            'archivos_app':files,'alcance':'Verificación Docker local, no despliegue Cloud Run ni IA real.'}
    (ROOT/args.salida).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['architecture','usuario','health_http','dashboard_http','ia_http','image_id']}))


if __name__=='__main__':main()
