import email
import django
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()

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

class TokenModelTest(TestCase):
    '''тест модели маркера'''

    def test_links_user_with_auto_generatied_uid(self):
        '''тест: соединяем пользователя с автогеренируемым uid'''
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
        