from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'romashev.al.s@gmail.com'
SUBJECT = 'Ваша ссылка на Суперзаписюльки'

class LoginTEst(FunctionalTest):
    '''тест регистрации в системе'''

    def test_can_get_mail_link_to_log_in(self):
        '''тест: моджно получить ссылку по почте для регистрации'''
        # Эдит заходит на опупительный сайт суперзаписюлек и впервые замечает раздел Войти
        # в навигационной панеле
        # Ее просят ввести свой адрес электронной почты, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # поялвтся сообщение, которое говорит, что ей на почту
        # было отправлено сообщение
        self.wait_for(lambda: self.assertIn(
            'Проверьте свою почту',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Эдит проверяет свою почту и находит сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит урл адрес
        self.assertIn('Используйте ссылку для входа', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Не найдена ссылка в письме:\n{email.body}')
        url=url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Выйти')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)