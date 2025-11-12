#!/bin/bash
# Script de inicialização da API

echo "🌐 Iniciando API FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
