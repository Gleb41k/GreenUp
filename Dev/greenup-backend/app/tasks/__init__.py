from .celery_app import celery_app
from .tasks import send_welcome_email  # ← КРИТИЧНО!

__all__ = ["celery_app", "send_welcome_email"]
