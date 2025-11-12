# 📦 Arquivos de Configuração Render

## 🎯 Visão Geral

Este projeto está configurado para deploy **separado e gratuito** no Render.

### Arquitetura:
```
┌─────────────┐
│  aneel-api  │ ← Web Service (render_api.yaml)
└──────┬──────┘
       ▼
┌─────────────┐
│aneel-redis  │ ← Redis Database (render_redis.yaml)
└──────┬──────┘
       ▼
┌─────────────┐
│aneel-worker │ ← Web Service rodando Celery (render_worker.yaml)
└─────────────┘

💰 Total: $0/mês
```

## 📁 Estrutura de Arquivos

```
projeto/
│
├── render_api.yaml          ← Config Blueprint API
├── render_worker.yaml       ← Config Blueprint Worker
├── render_redis.yaml        ← Config Blueprint Redis
│
├── start_api.sh             ← Script para iniciar API
├── start_worker.sh          ← Script para iniciar Worker (+ health check)
│
├── Dockerfile               ← Build da imagem Docker
├── requirements.txt         ← Dependências Python
├── docker-compose.yml       ← Apenas para dev local
│
├── INICIO_RAPIDO.md         ← Guia resumido 🚀
├── DEPLOY_RENDER_SEPARADO.md ← Guia completo passo a passo 📖
│
└── src/                     ← Código da aplicação
    ├── main.py
    ├── config/
    │   └── celery_app.py
    └── modules/
        └── aneel/
            └── aneel_tasks.py (com otimizações de memória)
```

## 🔧 Componentes

### 1. render_api.yaml
Configuração para o serviço da API:
- **Tipo:** Web Service
- **Runtime:** Docker
- **Comando:** `./start_api.sh`
- **Health Check:** `/`
- **Plano:** Free

**Variáveis necessárias:**
- `TENANT_ID`
- `CLIENT_ID_SUB`
- `CLIENT_SECRET_SUB`
- `REDIS_URL` (copiar do Redis após criá-lo)

### 2. render_redis.yaml
Configuração para o Redis:
- **Tipo:** Redis Database
- **Plano:** Free
- **Memória:** 25MB

**Importante:** Copie a "Internal Connection String" após criar.

### 3. render_worker.yaml
Configuração para o Worker:
- **Tipo:** Web Service (rodando Celery)
- **Runtime:** Docker
- **Comando:** `./start_worker.sh`
- **Health Check:** `/` (servidor HTTP simples)
- **Plano:** Free

**Variáveis necessárias:**
- `TENANT_ID`
- `CLIENT_ID_SUB`
- `CLIENT_SECRET_SUB`
- `REDIS_URL` (MESMA URL do Redis usada na API!)

### 4. start_api.sh
Script bash que inicia apenas o servidor FastAPI:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 5. start_worker.sh
Script bash que:
1. Inicia servidor HTTP na porta 8000 (para health check)
2. Inicia Celery worker em background

Isso permite que o Render veja o Worker como "healthy" mesmo sendo um worker.

## 🚀 Como Usar

### Opção 1: Guia Rápido
Leia: **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)**

### Opção 2: Guia Completo
Leia: **[DEPLOY_RENDER_SEPARADO.md](./DEPLOY_RENDER_SEPARADO.md)**

## ✅ Checklist de Deploy

- [ ] Código no GitHub
- [ ] Deploy API via `render_api.yaml`
- [ ] Adicionar variáveis do SharePoint na API
- [ ] Deploy Redis via `render_redis.yaml`
- [ ] Copiar REDIS_URL e adicionar na API
- [ ] Deploy Worker via `render_worker.yaml`
- [ ] Adicionar TODAS as variáveis no Worker (incluindo REDIS_URL)
- [ ] Testar health check da API
- [ ] Testar health check do Worker
- [ ] Criar job de teste
- [ ] Verificar logs do Worker

## 🔑 Variáveis de Ambiente

### API e Worker (ambos precisam):
```bash
TENANT_ID=seu_tenant_id
CLIENT_ID_SUB=seu_client_id
CLIENT_SECRET_SUB=seu_client_secret
REDIS_URL=redis://red-xxxxx:6379  # Copiar do Redis
```

### Automaticamente definidas pelo Render:
```bash
PORT=8000
PYTHON_VERSION=3.10
```

## 📊 Monitoramento

### Logs em Tempo Real:
1. Dashboard do Render
2. Clique no serviço (aneel-api, aneel-worker, etc)
3. Aba "Logs"

### Métricas:
1. Dashboard do Render
2. Clique no serviço
3. Aba "Metrics"
4. Veja RAM, CPU, etc.

### Health Checks:
```bash
# API
curl https://aneel-api-xxxx.onrender.com/

# Worker
curl https://aneel-worker-xxxx.onrender.com/
```

## 🆘 Troubleshooting Rápido

### API não conecta ao Redis
✅ Verifique se `REDIS_URL` está configurada corretamente

### Worker não processa tarefas
✅ Verifique se `REDIS_URL` do Worker é IGUAL à da API

### Out of Memory
✅ Otimizações já aplicadas em `aneel_tasks.py`
✅ Se persistir, considere Render Starter ($7/mês)

### Sleep (15 min de inatividade)
✅ Use cron-job.org para fazer ping a cada 10 min
✅ Completamente gratuito!

## 💡 Dicas

1. **Teste localmente primeiro** com Docker
2. **Anote** a REDIS_URL em local seguro
3. **Monitore** logs nas primeiras horas
4. **Configure** cron jobs para evitar sleep
5. **Backup** das variáveis de ambiente

## 🎯 Próximos Passos

Após deploy bem-sucedido:
1. Configure domínio customizado (opcional)
2. Configure monitoramento externo (UptimeRobot)
3. Configure notificações de erro
4. Considere upgrade se precisar de mais recursos

---

**Documentação atualizada em:** 12/11/2025  
**Custo Total:** $0/mês  
**Serviços:** 3 (API + Redis + Worker)
