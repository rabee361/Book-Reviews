from django.shortcuts import render
from .models import Book


def email_temp(request):
    book = Book.objects.all().order_by('?').first()
    context = {
        'book' : book
    }
    return render(request , 'bookapp/email.html' , context)