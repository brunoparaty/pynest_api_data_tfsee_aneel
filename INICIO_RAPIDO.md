# 🚀 COMECE AQUI - Deploy Render Separado

## Arquitetura

```
API (Web) + Redis (Database) + Worker (Web) = $0/mês
```

## ⚡ Início Rápido

### 1. Preparar (1 min)
```bash
git add .
git commit -m "Deploy separado Render"
git push origin main
```

### 2. Deploy (15 min total)

#### A) API (5 min)
1. render.com → New → Blueprint
2. Blueprint Path: `render_api.yaml`
3. Apply
4. Adicionar variáveis:
   - TENANT_ID
   - CLIENT_ID_SUB
   - CLIENT_SECRET_SUB

#### B) Redis (2 min)
1. render.com → New → Blueprint
2. Blueprint Path: `render_redis.yaml`
3. Apply
4. **Copiar** Internal Connection String
5. **Adicionar** REDIS_URL na API (Environment)

#### C) Worker (5 min)
1. render.com → New → Blueprint
2. Blueprint Path: `render_worker.yaml`
3. Apply
4. Adicionar **MESMAS** variáveis da API + REDIS_URL

### 3. Testar
```bash
curl https://aneel-api-xxxx.onrender.com/
```

## 📖 Documentação Completa

**[LEIA: DEPLOY_RENDER_SEPARADO.md](./DEPLOY_RENDER_SEPARADO.md)**

## 📁 Arquivos Importantes

- `render_api.yaml` - Config da API
- `render_worker.yaml` - Config do Worker  
- `render_redis.yaml` - Config do Redis
- `start_api.sh` - Inicia API
- `start_worker.sh` - Inicia Worker (com health check)
- `Dockerfile` - Build da imagem

## 💰 Custo

**$0/mês** (100% gratuito!)

## 🆘 Problemas?

1. Leia [DEPLOY_RENDER_SEPARADO.md](./DEPLOY_RENDER_SEPARADO.md) - seção Troubleshooting
2. Verifique logs no Dashboard do Render
3. Confirme que REDIS_URL é a MESMA em API e Worker

---

**Boa sorte! 🎉**
