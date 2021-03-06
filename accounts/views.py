from cmath import log
from email import message
import re
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.urls import reverse

from accounts.models import Token

def send_login_email(request):
    '''отправить сообщение для входа в систему'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login')+'?token='+str(token.uid)
    )
    message_body = f'Используйте ссылку для входа:\n\n{url}'
    send_mail(
        'Ваша ссылка на Суперзаписюльки', 
        message_body, 
        'python.testovich@mail.ru', 
        [email])
    messages.success(
        request,
        "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт."
    )
    return redirect('/')

def login(request):
    '''регистрируем вход в систему'''
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
    