from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import poplib
import os
import time

from .base import FunctionalTest

SUBJECT = 'Ваша ссылка на Суперзаписюльки'

class LoginTest(FunctionalTest):
    '''тест регистрации в системе'''

    def test_can_get_mail_link_to_log_in(self):
        '''тест: моджно получить ссылку по почте для регистрации'''
        # Эдит заходит на опупительный сайт суперзаписюлек и впервые замечает раздел Войти
        # в навигационной панеле
        # Ее просят ввести свой адрес электронной почты, что она и делает
        if self.staging_server:
            test_email = 'nars10@yandex.ru'
        else:
            test_email = 'Rtest@gmail.com'

        self.browser.get(self.live_server_url)
        
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # поялвтся сообщение, которое говорит, что ей на почту
        # было отправлено сообщение
        self.wait_for(lambda: self.assertIn(
            'Проверьте свою почту',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Эдит проверяет свою почту и находит сообщение
        body = self.wait_for_email(test_email, SUBJECT)
        # Оно содержит урл адрес
        self.assertIn('Используйте ссылку для входа', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Не найдена ссылка в письме:\n{body}')
        url=url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе
        self.wait_to_be_logged_in(email=test_email)

        #теперь она выходит из системы
        self.browser.find_element_by_link_text('Выйти').click()

        # Она вышла из системы
        self.wait_to_be_logged_out(email=test_email)


    def wait_for_email(self, test_email, subject):
        '''ожидать электронное сообщение'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.yandex.ru')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YANDEX_PASSWORD'])
            while time.time() - start < 60:
                #получить 10 новых сообщений
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count-10), count +1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()



