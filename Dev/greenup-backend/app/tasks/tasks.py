from app.core.logger.factory import get_logger
from app.tasks.celery_app import celery_app

# Получаем логгер
logger = get_logger()


@celery_app.task(bind=True, name="send_welcome_email")
def send_welcome_email(self, email: str):
    """
    Отправляет приветственное письмо.
    В реальности — вызов SMTP, SendGrid, etc.
    """
    logger.info("Sending welcome email", {"email": email, "task_id": self.request.id})

    # Здесь будет реальная отправка
    # send_email_via_smtp(email, "Welcome!", "Hello!")

    logger.debug("Welcome email sent (simulated)", {"email": email})
