import smtplib
from pathlib import Path
from PIL import Image
from app.config import SMTP_PORT, SMTP_HOST, SMTP_USER, SMTP_PASS
from pydantic import EmailStr

from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_tempalte


@celery.task
def process_pic(
        path: str,
):
    in_path = Path(path)
    im = Image.open(in_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500 = save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100 = save(f"app/static/images/resized_200_100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    email_to_mock = SMTP_USER
    msg_content = create_booking_confirmation_tempalte(booking, email_to_mock)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)

