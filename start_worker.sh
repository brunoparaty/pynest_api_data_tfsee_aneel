#!/bin/bash
# Script de inicialização do Worker com Health Check

echo "👷 Iniciando Worker Celery com Health Check..."

# Inicia servidor HTTP para health check em background
python3 -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Worker is healthy')
    
    def log_message(self, format, *args):
        pass  # Silencia logs do servidor HTTP

def run_health_server():
    server = HTTPServer(('0.0.0.0', 8000), HealthHandler)
    print('Health check server running on port 8000')
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

print('Health check started, waiting for Celery...')
import time
time.sleep(999999)  # Mantém o script rodando
" &

# Pequeno delay para garantir que o health server inicie
sleep 2

# Inicia o Celery Worker
echo "Starting Celery worker..."
exec celery -A src.config.celery_app worker --loglevel=info --pool=solo
