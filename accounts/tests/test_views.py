from urllib import response
from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token

import accounts.views

class SendLoginEmailViewTest(TestCase):
    '''тест представления, которое отправляет
    сообщение для входа в систему'''

    def test_redirect_to_home_page(self):
        '''тест: перенаправление на домашнюю страницу'''
        response = self.client.post('/accounts/send_login_email', data={
            'email':'test@gmail.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_mail_to_address_from_post(self, mock_send_mail):
        # '''тест:отправляет сообщение на адрес из метода post'''
        # self.send_mail_called = False

        # def fake_send_mail(subject, body, from_email, to_list):
        #     '''поддельная функция send_mail'''
        #     self.send_mail_called = True
        #     self.subject = subject
        #     self.body = body
        #     self.from_email = from_email
        #     self.to_list = to_list

        # accounts.views.send_mail = fake_send_mail

        self.client.post('/accounts/send_login_email', data={
            'email':'test@gmail.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(subject, 'Ваша ссылка на Суперзаписюльки')
        self.assertEqual(from_email, 'python.testovich@mail.ru')
        self.assertEqual(to_list, ['test@gmail.com'])


    def test_adds_success_message(self):
        '''тест: добавляется сообщение об успехе'''
        response = self.client.post('/accounts/send_login_email', data={
            'email':'test@gmail.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт."
        )

        self.assertEqual(message.tags, "success")

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        '''тест: отсылается ссылка для входа в систему, использую маркер uid'''
        self.client.post('/accounts/send_login_email', data={
            'email':'test@gmail.com'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs=mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_creates_token_associated_with_email(self):
        '''тест: создается маркер, связаный с электронной почтой'''
        self.client.post('/accounts/send_login_email', data={
            'email':'test@gmail.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'test@gmail.com')

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    '''тест представления входа в систему'''

    def test_redirect_to_home_pahe(self, mock_auth):
        '''тест: переадресуется на домашнюю страницу'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        '''тест: вызывается аутентификейт с уидом из гет-запроса'''
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        '''тест: вызывается auth_login с пользователем если такой имеется'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        '''тест: не регистрируется в системе, если пользователь не аутентифицирован'''
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)