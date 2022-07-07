import email
from urllib import request
import django
from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import get_user_model

from accounts.models import Token

User = auth.get_user_model()

class UserModelTest(TestCase):
    '''тест модели пользователя'''

    def test_user_is_valid_with_email_only(self):
        '''тест: пользователь допустим только с электронной почты'''
        user = User(email='a@b.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        '''тест: адрес электронной почты является первичным ключом'''
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        '''тест: проблем с auth_login нет'''
        user = User.objects.create(email = 'test@gmail.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)

class TokenModelTest(TestCase):
    '''тест модели маркера'''

    def test_links_user_with_auto_generatied_uid(self):
        '''тест: соединяем пользователя с автогеренируемым uid'''
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
        