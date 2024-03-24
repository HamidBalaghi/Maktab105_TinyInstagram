from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'OTP Verification'
        message = f'Welcome to Our Tiny Instagram\nDear {instance.name},\n\nYour OTP is {instance.otp}'
        from_email = 'balaghi.hamid.django@gmail.com'
        to_email = instance.email
        send_mail(subject, message, from_email, [to_email])
