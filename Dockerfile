# Imagem base oficial do Playwright
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# --- NOVA ETAPA ---
# Instala o pacote 'iproute2', que contém o comando 'ip' exigido pela pynest-api
# O apt-get update atualiza a lista de pacentes e o -y confirma a instalação.
RUN apt-get update && apt-get install -y iproute2 && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Instala os navegadores do Playwright
RUN python -m playwright install --with-deps chromium

# Copia scripts de inicialização e dá permissão de execução
COPY start_api.sh start_worker.sh ./
RUN chmod +x start_api.sh start_worker.sh

# --- NOVA ETAPA: Boas Práticas de Segurança ---
# Cria um usuário não-root chamado 'appuser' para rodar a aplicação
RUN useradd --create-home appuser
# Muda o proprietário dos arquivos da aplicação para o novo usuário
RUN chown -R appuser:appuser /app
# Define o novo usuário como o padrão para os comandos seguintes
USER appuser

# Expõe a porta da API
EXPOSE 8000