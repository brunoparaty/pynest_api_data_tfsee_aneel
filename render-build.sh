#!/bin/bash
set -e

echo "🔄 Inicializando submódulos Git..."
git submodule update --init --recursive

echo "✅ Submódulos inicializados com sucesso!"
