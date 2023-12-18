from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config import celery_app

# from profis.utils.eskiz import SMSClient

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def send_otp_by_phone(otp, phone_number):
    # client = SMSClient(
    #     api_url="https://notify.eskiz.uz/api/",
    #     email="test@eskiz.uz",
    #     password="j6DWtQjjpLDNjWEk74Sx",
    # )
    # resp = client._send_sms(phone_number=phone_number, message=otp)
    send_code_on_telegram(otp)
    resp = print(f"{otp} sent to {phone_number}")
    return resp


@celery_app.task()
def send_otp_by_email(otp, email):
    resp = f"{otp} sent to {email}"
    send_mail(subject="otp", message=resp, from_email="se", recipient_list=[email])
    return resp


def send_code_on_telegram(security_code):
    """
    Sending security code to telegram channel for testing purpose
    """
    import telebot

    bot = telebot.TeleBot("5393375054:AAFCLPFARn3GLIyZp_eI1c8YIWOvnpwda7s", parse_mode="HTML")
    bot.send_message(
        chat_id=-1001541588192,
        text=f"Используйте код <strong>{security_code}</strong> для авторизации",
    )
