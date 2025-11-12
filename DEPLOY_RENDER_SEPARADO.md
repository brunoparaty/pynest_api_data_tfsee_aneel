# 🚀 Guia Completo - Deploy Separado no Render (100% Grátis)

## 🎯 Arquitetura que Vamos Criar

```
┌─────────────────────────────┐
│  Projeto 1: aneel-api       │
│  (Web Service - Free)       │
│  └─ FastAPI                 │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Projeto 2: aneel-redis     │
│  (Redis Database - Free)    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Projeto 3: aneel-worker    │
│  (Web Service - Free)       │
│  └─ Celery Worker           │
└─────────────────────────────┘

💰 CUSTO: $0/mês (3 serviços gratuitos!)
```

---

## 📋 Pré-requisitos

- ✅ Conta no [Render](https://render.com) (gratuita)
- ✅ Conta no GitHub
- ✅ Código enviado para GitHub
- ✅ Credenciais do SharePoint (TENANT_ID, CLIENT_ID_SUB, CLIENT_SECRET_SUB)

---

## 🚀 Passo a Passo

### Passo 0: Preparar o Código

```bash
# 1. Adicionar todos os arquivos
git add .

# 2. Commitar
git commit -m "Configuração para deploy separado no Render"

# 3. Enviar para GitHub
git push origin main
```

---

### Passo 1: Deploy da API (5 minutos)

1. **Acesse:** https://dashboard.render.com/
2. **Clique em:** "New" → "Blueprint"
3. **Conecte** seu repositório GitHub: `pynest_api_data_tfsee_aneel`
4. **Quando aparecer "Blueprint detected":**
   - Name: `aneel-api-blueprint`
   - **IMPORTANTE:** Mude o campo "Blueprint Spec Path" para: `render_api.yaml`
5. **Clique em:** "Apply"
6. **Aguarde** o build (~10-15 minutos)

#### Configurar Variáveis de Ambiente da API

Quando o build terminar:

1. Vá em **"aneel-api"** (o serviço criado)
2. Clique na aba **"Environment"**
3. **Adicione as variáveis:**
   ```
   TENANT_ID = seu_valor_aqui
   CLIENT_ID_SUB = seu_valor_aqui
   CLIENT_SECRET_SUB = seu_valor_aqui
   ```
4. Clique em **"Save Changes"**

⚠️ **IMPORTANTE:** Guarde a URL da API! Algo como:
```
https://aneel-api-xxxx.onrender.com
```

✅ **API pronta!** Mas ainda não funciona (falta Redis).

---

### Passo 2: Deploy do Redis (2 minutos)

1. No Dashboard do Render, clique em **"New" → "Blueprint"**
2. Conecte o **mesmo repositório** GitHub
3. **Quando aparecer "Blueprint detected":**
   - Name: `aneel-redis-blueprint`
   - **IMPORTANTE:** Mude "Blueprint Spec Path" para: `render_redis.yaml`
4. Clique em **"Apply"**
5. **Aguarde** (~1 minuto para criar Redis)

#### Copiar URL do Redis

Quando terminar:

1. Vá em **"aneel-redis"** (o serviço criado)
2. Na página inicial do serviço, você verá **"Internal Connection String"**
3. **Copie** a URL completa (algo como):
   ```
   redis://red-xxxxxxxxxxxxx:6379
   ```

#### Adicionar Redis URL na API

1. Volte para o serviço **"aneel-api"**
2. Vá em **"Environment"**
3. Clique em **"Add Environment Variable"**
4. **Adicione:**
   ```
   Key: REDIS_URL
   Value: redis://red-xxxxxxxxxxxxx:6379  (cole a URL que você copiou)
   ```
5. Clique em **"Save Changes"**
6. O serviço vai reiniciar automaticamente

✅ **Redis conectado à API!**

---

### Passo 3: Deploy do Worker (5 minutos)

1. No Dashboard, clique em **"New" → "Blueprint"**
2. Conecte o **mesmo repositório** GitHub novamente
3. **Quando aparecer "Blueprint detected":**
   - Name: `aneel-worker-blueprint`
   - **IMPORTANTE:** Mude "Blueprint Spec Path" para: `render_worker.yaml`
4. Clique em **"Apply"**
5. **Aguarde** o build (~10-15 minutos)

#### Configurar Variáveis do Worker

Quando terminar:

1. Vá em **"aneel-worker"** (o serviço criado)
2. Clique na aba **"Environment"**
3. **Adicione TODAS as variáveis:**
   ```
   TENANT_ID = seu_valor_aqui
   CLIENT_ID_SUB = seu_valor_aqui
   CLIENT_SECRET_SUB = seu_valor_aqui
   REDIS_URL = redis://red-xxxxxxxxxxxxx:6379  (MESMA URL do passo anterior!)
   ```
4. Clique em **"Save Changes"**

✅ **Worker pronto e conectado!**

---

## ✅ Verificar se Está Funcionando

### 1. Testar Health Check da API

```bash
curl https://aneel-api-xxxx.onrender.com/
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "message": "ANEEL Jobs API is running!"
}
```

### 2. Testar Health Check do Worker

```bash
curl https://aneel-worker-xxxx.onrender.com/
```

**Resposta esperada:**
```
Worker is healthy
```

### 3. Criar um Job de Teste

```bash
curl -X POST https://aneel-api-xxxx.onrender.com/aneel-jobs/pdf-generation \
  -H "Content-Type: application/json" \
  -d '{"search_term": "TESTE"}'
```

**Resposta esperada:**
```json
{
  "mensagem": "Tarefa de automação iniciada com sucesso.",
  "id_da_tarefa": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 4. Verificar Status do Job

```bash
# Substitua ID_DA_TAREFA pelo id retornado acima
curl https://aneel-api-xxxx.onrender.com/aneel-jobs/ID_DA_TAREFA
```

**Resposta esperada (processando):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "STARTED",
  "resultado": "A tarefa ainda está sendo processada."
}
```

### 5. Ver Logs do Worker

1. No Dashboard do Render
2. Vá em **"aneel-worker"**
3. Clique na aba **"Logs"**
4. Procure por:
   ```
   WORKER: Iniciando automação para o CNPJ: 'TESTE'...
   ```

✅ **Se aparecer isso, está funcionando perfeitamente!**

---

## 📊 Resumo dos 3 Serviços

| Serviço | Tipo | URL | Função |
|---------|------|-----|--------|
| **aneel-api** | Web Service | https://aneel-api-xxxx.onrender.com | Recebe requisições HTTP |
| **aneel-redis** | Redis | redis://red-xxx:6379 | Fila de mensagens |
| **aneel-worker** | Web Service | https://aneel-worker-xxxx.onrender.com | Processa tarefas |

---

## 🔄 Como Fazer Atualizações

Sempre que você fizer alterações no código:

```bash
git add .
git commit -m "Descrição da alteração"
git push origin main
```

**Render faz deploy automático!** 🎉

Para desabilitar deploy automático:
- Em cada serviço → Settings → Build & Deploy → Auto-Deploy → OFF

---

## ⚠️ Limitações do Plano Gratuito

### API e Worker:
- **Sleep:** Após 15 minutos de inatividade
- **Cold Start:** ~30 segundos na primeira requisição após sleep
- **RAM:** 512MB cada
- **CPU:** Compartilhada

### Redis:
- **Memória:** 25MB
- **Conexões:** Limitadas
- **Persistência:** Não garantida (pode perder dados)

### Solução para Sleep:

Use [cron-job.org](https://cron-job.org) (gratuito):
1. Crie 2 jobs:
   - URL API: `https://aneel-api-xxxx.onrender.com/`
   - URL Worker: `https://aneel-worker-xxxx.onrender.com/`
2. Intervalo: A cada 10 minutos
3. Serviços ficam sempre ativos! 🎉

---

## 🆘 Troubleshooting

### API não inicia
✅ **Verificar:**
- Logs: aneel-api → Logs
- Variáveis de ambiente configuradas?
- REDIS_URL está correta?

### Worker não processa tarefas
✅ **Verificar:**
- Logs: aneel-worker → Logs
- Procure por "Iniciando Worker Celery"
- REDIS_URL é a MESMA da API?
- Credenciais do SharePoint corretas?

### Build falha
✅ **Verificar:**
- Dockerfile está correto?
- start_api.sh e start_worker.sh estão no repositório?
- requirements.txt tem todas as dependências?

### Out of Memory
✅ **Soluções:**
1. As otimizações já foram aplicadas no código
2. Se persistir, considere Render Starter ($7/mês) para 2GB RAM
3. Ou migre para Fly.io (mais RAM grátis)

### Redis desconectado
✅ **Verificar:**
- Redis está rodando? (Dashboard → aneel-redis → Status)
- REDIS_URL está configurada em AMBOS (API e Worker)?
- URLs são EXATAMENTE iguais?

---

## 💡 Dicas Importantes

### 1. Monitorar Recursos
- Dashboard → Cada serviço → "Metrics"
- Acompanhe uso de RAM e CPU

### 2. Logs em Tempo Real
- Dashboard → Serviço → "Logs"
- Veja erros e debug em tempo real

### 3. Testar Localmente Primeiro
```bash
# Simule ambiente Render localmente
docker build -t aneel-test .

# API
docker run -p 8000:8000 -e REDIS_URL=redis://localhost:6379 \
  aneel-test bash start_api.sh

# Worker (outro terminal)
docker run -e REDIS_URL=redis://localhost:6379 \
  aneel-test bash start_worker.sh
```

### 4. Backup das Variáveis de Ambiente
Anote suas variáveis em local seguro:
```
TENANT_ID=...
CLIENT_ID_SUB=...
CLIENT_SECRET_SUB=...
REDIS_URL=redis://red-xxxxx:6379
```

---

## 🎯 Checklist Final

- [ ] API deployada e rodando
- [ ] Redis criado
- [ ] REDIS_URL adicionada na API
- [ ] Worker deployado
- [ ] REDIS_URL adicionada no Worker (MESMA URL!)
- [ ] Variáveis do SharePoint em ambos
- [ ] Health check da API funcionando
- [ ] Health check do Worker funcionando
- [ ] Job de teste criado
- [ ] Worker processou o job (ver logs)
- [ ] (Opcional) Cron jobs configurados

---

## 🎉 Pronto!

Você agora tem:
- ✅ API e Worker **separados**
- ✅ Arquitetura **escalável**
- ✅ **100% gratuito** ($0/mês)
- ✅ **Isolamento** de falhas
- ✅ **Monitoramento** independente

**Custo Total: $0/mês para sempre!** 🎉

---

## 📚 Próximos Passos (Opcional)

1. **Domínio Customizado:**
   - Settings → Custom Domain
   - Configure CNAME no seu DNS

2. **Monitoramento Externo:**
   - [UptimeRobot](https://uptimerobot.com) - Gratuito
   - Monitore disponibilidade

3. **Notificações:**
   - Settings → Notifications
   - Adicione email ou Discord webhook

4. **Upgrade (se necessário):**
   - Worker para Starter: $7/mês (2GB RAM)
   - Melhor performance para Playwright

---

**Boa sorte com o deploy! 🚀**

Se tiver dúvidas, consulte os logs ou entre em contato com o suporte do Render.
