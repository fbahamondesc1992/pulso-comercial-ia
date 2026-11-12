FROM python:3.12.15-slim@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080 AI_ENABLED=false
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home pulso
COPY app.py validador_csv.py indicadores.py schemas.py analista_ia.py ./
COPY templates/ templates/
COPY static/ static/
COPY datos/demo_ventas.csv datos/demo_ventas.csv
COPY prompts/analista_v1.md prompts/analista_v2.md prompts/
USER 10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8080')+'/health', timeout=2)"
# Un proceso: los límites son por proceso. No activar --preload ni más workers sin rediseñar cuotas.
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --worker-class gthread --threads 4 --timeout 65 --access-logfile /dev/null app:app"]
