from celery import Celery
import os


celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

# Автоматический поиск задач в файлах tasks.py
celery_app.autodiscover_tasks(["app.services"])


