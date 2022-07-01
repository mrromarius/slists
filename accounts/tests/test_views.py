from django.test import TestCase
from unittest.mock import patch

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
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['test@gmail.com'])

