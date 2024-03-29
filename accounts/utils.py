from .models import User
import random
from django.utils import timezone
from django.core.mail import send_mail


def otp_sender(user: User):
    otp = random.randint(100000, 999999)
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()
    subject = 'OTP Verification'
    message = f'Welcome to Our Tiny Instagram\nDear {user.name},\n\nYour OTP is {otp}'
    from_email = 'balaghi.hamid.django@gmail.com'
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])
