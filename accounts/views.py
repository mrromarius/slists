import email
from plistlib import UID
import uuid
import sys
from django.shortcuts import render
from django.core.mail import send_mail

from accounts.models import Token


def send_login_email(request):
    '''выслать ссылку на логин по почте'''
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('uid сохранен', uid, 'для почты', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Ваш login для доступа к Задачам',
        f'Используйте ссылку для подключения:',
        'noreply@superlists',
        [email],
    )
    return render(request, 'login_email_send.mail')
