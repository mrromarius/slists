import email
from django.shortcuts import render

from django.core.mail import send_mail
from django.shortcuts import redirect

def send_login_email(request):
    '''отправить сообщение для входа в систему'''
    email = request.POST['email']
    send_mail(
        'Ваша ссылка на Суперзаписюльки', 
        'Тело письма', 
        'noreply@superlists', 
        [email])
    return redirect('/')