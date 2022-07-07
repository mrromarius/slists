import email
from lib2to3.pgen2 import token
from unittest import result
from urllib import request
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User

User = get_user_model()

class AuthenticateTest(TestCase):
    '''тест аутентификации'''

    def test_returns_None_if_no_such_token(self):
        '''тест: Возвращает None, если нет такого маркера'''
        result = PasswordlessAuthenticationBackend().authenticate(
            request,
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''тест: возвращает нового пользователя с правильной почтой
        если маркер существует'''

        email = 'test@gmail.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        '''тест: возвращает существующего пользователя с правильной почтой
        если маркер существует'''

        email = 'test@gmail.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(request, token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    '''тест получения пользователя'''

    def test_gets_user_by_email(self):
        '''тест: получает пользователя по адресу электронной почты '''
        User.objects.create(email='another@gmail.com')
        desired_user = User.objects.create(email='test@gmail.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'test@gmail.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        '''тест: возвращает None, если нет поьзователя с такой почтой'''
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('test@gmail.com')
        )
