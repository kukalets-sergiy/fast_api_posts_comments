# test_celery.py
from app.tasks import auto_reply_task

result = auto_reply_task.delay(1, 2)
print(result.get(timeout=3))
