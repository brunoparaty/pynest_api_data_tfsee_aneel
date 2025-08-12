import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# O broker e o backend apontam para o nosso Redis rodando no Docker
app = Celery(
    'aneel_tasks',
    broker=redis_url,
    backend=redis_url,
    include=['src.modules.aneel.aneel_tasks'] # << Aponta onde estão as tarefas
)

app.conf.update(
    task_track_started=True,
)