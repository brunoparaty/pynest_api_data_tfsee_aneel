# API de Automação ANEEL TFSEE

API assíncrona para automatizar a busca e o download de Guias de Recolhimento da União (GRU) da Taxa de Fiscalização de Serviços de Energia Elétrica (TFSEE) do site da ANEEL.

## 🚀 Funcionalidades

- **Download de Boletos em Lote:** Realiza uma busca e processa todas as empresas encontradas, baixando um PDF para cada uma e envia para o Sharepoint.
- **Extração Rápida de Dados:** Um endpoint síncrono para obter apenas as informações do boleto (valor, vencimento) em formato JSON.
- **Processamento Assíncrono:** Utiliza Celery e Redis para executar as automações pesadas em segundo plano, mantendo a API sempre rápida e responsiva.


## 🏛️ Arquitetura

Este projeto utiliza uma arquitetura de microserviços desacoplada para lidar com tarefas de longa duração (web scraping com Playwright).

- **API (PyNest + Uvicorn):** Recebe as requisições HTTP, valida os dados e delega o trabalho pesado.
- **Fila de Tarefas (Redis):** Atua como um "broker" de mensagens, armazenando as tarefas que precisam ser executadas.
- **Worker (Celery + Playwright):** Um processo separado que consome as tarefas da fila, inicia um navegador headless com Playwright, executa a automação no site da ANEEL e salva os resultados.


## ⚙️ Endpoints da API

A URL base da API é `http://localhost:8000`.

### Health Check

Verifica se a API está no ar.

- **GET** `http://127.0.0.1:8000/`
  - **Resposta de Sucesso (200 OK):**
    ```json
    {
      "status": "ok",
      "message": "ANEEL Jobs API is running!"
    }
    ```

### Automação de Boletos (Jobs)

#### Iniciar Geração de PDFs (Assíncrono)

Inicia a automação completa com Playwright para baixar os PDFs.

- **POST** `/aneel-jobs/pdf-generation`
  - **Corpo da Requisição (JSON):**
    ```json
    {
      "search_term": "NOME DA EMPRESA"
    }
    ```
  - **Resposta Imediata (200 OK):**
    ```json
    {
      "mensagem": "Tarefa de automação iniciada com sucesso.",
      "id_da_tarefa": "uuid-da-tarefa-gerado-pelo-celery"
    }
    ```

#### Verificar Status de um Job

Verifica o progresso e o resultado de uma tarefa iniciada.

- **GET** `/aneel-jobs/{job_id}`
  - **Resposta (Tarefa em Andamento):**
    ```json
    {
      "id": "uuid-da-tarefa",
      "status": "STARTED",
      "resultado": "A tarefa ainda está sendo processada."
    }
    ```
  - **Resposta (Tarefa Concluída com Sucesso):**
    ```json
    {
      "id": "uuid-da-tarefa",
      "status": "SUCCESS",
      "resultado": {
        "sucesso": true,
        "relatorio": [
          {
            "empresa": "NOME DA EMPRESA LTDA - CNPJ: ...",
            "status": "Sucesso",
            "arquivo": "Boletos_PDF_ANEEL/Boleto_PDF_... .pdf"
          }
        ]
      }
    }
    ```

#### Extrair Dados do Boleto (Síncrono)

Busca rapidamente os dados do boleto (valor, vencimento) e retorna um JSON.

- **GET** `/aneel-jobs/data-extraction`
  - **Parâmetro de Busca (Query Param):**
    `?search_term=NOME DA EMPRESA`
  - **URL Completa:** `http://localhost:8000/aneel-jobs/data-extraction?search_term=CERRADAO`
  - **Resposta de Sucesso (200 OK):**
    ```json
    {
      "sucesso": true,
      "relatorio": [
        {
          "empresa": "NOME DA EMPRESA LTDA - CNPJ: ...",
          "status": "Sucesso",
          "valor_boleto": 18432.6,
          "data_vencimento": "15/08/2025",
          "mes_competencia": "07/2025"
        }
      ]
    }
    ```

## 📋 Pré-requisitos

- Python 3.9+
- Docker e Docker Compose

## 🚀 Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ParatyEnergia/project-paraty-next.git
    ```

2. **Crie e configure o arquivo de ambiente:**
    - Renomeie (ou copie) o arquivo `env.example` para `.env`.
    - Preencha o arquivo `.env` com as suas credenciais.
    ```bash
    TENANT_ID=SEU_TENANT_ID
    CLIENT_ID_SUB=SEU_CLIENT_ID
    CLIENT_SECRET_SUB=SEU_CLIENT_SECRET
    ```

3. **Inicializar o Submódulo:**
    ```bash
    git submodule update --init --recursive
    ```

3.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux / macOS
    source .venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Instale os navegadores do Playwright:**
    ```bash
    python -m playwright install
    ```

6.  **Inicie o Redis com Docker:**
    *Verifique se o Docker Desktop está rodando.*
    ```bash
    docker-compose up -d
    ```

### Como Rodar a Aplicação

Para rodar a aplicação, você precisa de **dois terminais abertos** na pasta raiz do projeto.

**1. No Terminal 1, inicie o Worker do Celery:**
   *Este processo é o "chef" que executa as automações.*
   ```bash
   celery -A src.config.celery_app worker --loglevel=info --pool=solo
   ```
**2. No Terminal 2, inicie a API PyNest:** 
    *Este processo é o "garçom" que recebe as requisições.*
   ```bash
   uvicorn src.main:app --reload
   ```

A API estará disponível em http://127.0.0.1:8000.