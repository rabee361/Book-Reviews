from celery import shared_task
from django.core.mail import send_mail , send_mass_mail
from .models import Message , Book
from django.contrib.auth.models import User
from django.conf import settings    
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

# @shared_task
# def send_book():
#     book = Book.objects.all().order_by('?').first()

#     with open(book.cover.path, 'rb') as img_file:
#         img_base64 = base64.b64encode(img_file.read()).decode()

#     from_email = settings.DEFAULT_FROM_EMAIL
#     context = {
#         'book': book,
#         'img_data': img_base64,
#     }
#     html_ = render_to_string('bookapp/email.html', context)
#     sent_mail = send_mail(
#     "testing",
#     "im testing now",
#     from_email,
#     ['john1986moore@gmail.com'],
#     html_message=html_,
#     fail_silently=False,
# )
#     return sent_mail


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

@shared_task
def send_book():
    book = Book.objects.all().order_by('?').first()
    users = User.objects.values_list('email',flat=True).all()
    subject = "testing"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = users

    context = {
        'book': book,
    }
    html_content = render_to_string('bookapp/email.html', context)

    # Create the email
    email = EmailMultiAlternatives(subject, html_content, from_email, to)
    email.content_subtype = "html"  # Main content is now text/html

    # Open the image, read it and attach it to the email
    with open(book.cover.path, 'rb') as img:
        msg_image = MIMEImage(img.read())
        msg_image.add_header('Content-ID', '<{}>'.format(book.cover.name))
        email.attach(msg_image)

    # Send the email
    sent_mail = email.send(fail_silently=False)

    return sent_mail