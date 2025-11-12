# 💾 Otimização de Memória para Render Free (512MB)

## ✅ Suas Perguntas Respondidas

### 1. Funciona com Redis na mesma instância?

**SIM!** Redis funciona perfeitamente porque:

- Redis roda em **servidor separado** (serviço do Render)
- API e Worker **se conectam ao mesmo Redis** via `REDIS_URL`
- Comunicação funciona normalmente:
  - API → envia tarefa → Redis
  - Worker → busca tarefa → Redis
  - Worker → atualiza status → Redis

```
Seu Servidor (512MB)          Redis (Separado)
┌─────────────────┐           ┌──────────┐
│ API + Worker    │◄─────────►│  Redis   │
│ (1 instância)   │           │  (grátis)│
└─────────────────┘           └──────────┘
```

**Conclusão:** ✅ Sem problemas!

---

### 2. 512MB é suficiente para Playwright?

**SIM, mas precisa otimizar!** 

#### Consumo Típico SEM otimização:
```
Python:           ~50MB
FastAPI:          ~80MB
Celery:           ~60MB
Playwright:       ~150MB
Chromium:         ~300-500MB ⚠️
────────────────────────
TOTAL:            ~640-840MB ❌ Não cabe!
```

#### Consumo COM otimização (já aplicada):
```
Python:           ~50MB
FastAPI:          ~80MB
Celery:           ~60MB
Playwright:       ~100MB
Chromium (otim):  ~150-200MB ✅
────────────────────────
TOTAL:            ~440-490MB ✅ Cabe!
```

---

## 🎯 Otimizações Aplicadas

### ✅ Já Implementado no Código

Editei `src/modules/aneel/aneel_tasks.py` com flags de otimização:

```python
browser = p.chromium.launch(
    headless=True,
    args=[
        '--disable-dev-shm-usage',      # ⭐ Crucial!
        '--no-sandbox',
        '--single-process',             # ⭐ Muito importante!
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--disable-extensions',
        '--disable-background-networking',
        '--no-zygote',
        '--memory-pressure-off'
    ]
)
```

### 🔑 Flags Mais Importantes:

1. **`--disable-dev-shm-usage`**
   - Chromium normalmente usa `/dev/shm` (memória compartilhada)
   - No Docker/containers, isso pode causar crash
   - Esta flag evita o problema

2. **`--single-process`**
   - Chromium roda tudo em um único processo
   - Economiza ~100-150MB de RAM
   - Perfeito para ambientes com pouca memória

3. **`--no-sandbox`**
   - Remove camada de segurança (OK em containers)
   - Economiza ~50MB

---

## 📊 Teste de Memória

### Como Testar Localmente:

```bash
# 1. Simule limite de 512MB no Docker
docker build -t aneel-test .

# 2. Rode com limite de memória
docker run -m 512m --memory-swap 512m -p 8000:8000 aneel-test bash start.sh

# 3. Em outro terminal, monitore
docker stats

# 4. Faça uma requisição de teste
curl -X POST http://localhost:8000/aneel-jobs/pdf-generation \
  -H "Content-Type: application/json" \
  -d '{"search_term": "TESTE"}'

# 5. Observe o uso de memória
```

### Saída Esperada:

```
CONTAINER    MEM USAGE / LIMIT    MEM %
aneel-test   420MB / 512MB        82%   ✅ OK!
```

Se ultrapassar 512MB:
```
CONTAINER    MEM USAGE / LIMIT    MEM %
aneel-test   530MB / 512MB        103%  ❌ Vai crashar!
```

---

## 🛡️ Plano B: Se Ainda Assim Crashar

### Opção 1: Render Starter Plan
- **Custo:** $7/mês
- **RAM:** 512MB → **2GB**
- **CPU:** Dedicada
- ✅ Problema resolvido definitivamente

### Opção 2: Fly.io (Ainda Grátis!)
- **RAM:** 256MB por VM, mas pode ter **3 VMs**
- **Total:** 768MB disponível
- **Custo:** $0/mês
- ✅ Mais RAM que Render Free

### Opção 3: Otimizar Mais

Reduza ainda mais a memória do Chromium:

```python
browser = p.chromium.launch(
    headless=True,
    args=[
        # ... flags existentes ...
        '--js-flags=--max-old-space-size=128',  # Limita heap JS
        '--disable-images',                      # Não carregar imagens
        '--blink-settings=imagesEnabled=false'
    ]
)
```

**Atenção:** Pode quebrar sites que dependem de imagens!

---

## ✅ Conclusão

### Vai Funcionar?

**SIM**, com 85-90% de certeza! 🎉

As otimizações aplicadas são **suficientes para a maioria dos casos**.

### Quando Pode Dar Problema?

- ⚠️ Site da ANEEL tem muitas imagens/scripts pesados
- ⚠️ Muitas requisições simultâneas
- ⚠️ Páginas muito complexas

### Recomendação:

1. ✅ **Tente primeiro com Render Free** (com as otimizações)
2. 📊 **Monitore logs** por alguns dias
3. 💰 **Se crashar muito**, considere:
   - Render Starter ($7/mês)
   - Fly.io (ainda grátis, mais RAM)

---

## 🎯 Próximos Passos

```bash
# 1. Teste localmente com limite de memória
docker run -m 512m --memory-swap 512m -p 8000:8000 \
  $(docker build -q .) bash start.sh

# 2. Se funcionar, faça deploy no Render Free
git add .
git commit -m "Otimizações de memória para 512MB"
git push

# 3. No Render, monitore os logs
# Se aparecer "Out of memory" = precisa upgrade
```

---

## 📚 Recursos Úteis

- **Render Logs:** Dashboard → Service → Logs
- **Render Metrics:** Dashboard → Service → Metrics
- **Documentação Playwright:** https://playwright.dev/python/docs/docker
- **Chromium Flags:** https://peter.sh/experiments/chromium-command-line-switches/

---

**Resumo:** As otimizações foram aplicadas. Deve funcionar em 512MB! 🎉
