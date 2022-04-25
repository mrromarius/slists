import fractions
import sys
import time
import unittest
from sys import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    '''тест нового посетителя'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''уничтожение'''
        self.browser.quit()

    def wait_for_row_in_list_tabel(self, row_text):
        '''подтверждение строки в таблице списка'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_layout_and_styling(self):
        '''тест макета стилевого оформления'''
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она замечает что поле ввода аккуратно отцетровано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
            )
        
        # Она начинает новый список и видит что там поле тоже центрировано
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )



    def test_can_start_a_list_for_one_user(self):
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Начать новый список задач', header_text)

        # ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Введите элемент списка'
        )

        # она выбирает в текстовом поле "купить павлиньи перья" (ее хобби - вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # когда она нажимает ентер, страница обновляется, и теперь страница содержит
        # "1. купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_tabel('1. Купить павлиньи перья')
        # текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # она заводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методичка)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # страница сново обновляется, и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_tabel('1. Купить павлиньи перья')
        self.wait_for_row_in_list_tabel(
            '2. Сделать мушку из павлиньих перьев')
        # Эдит интересно, запомнит ли сайт ее спсико. Далее она видит, что
        # сайт сгенерировал для нее уникальный УРЛ-адрес об этом
        # выводится небольшой текст с объяснениями.
        

        # она посещяет этот УРЛ адрес- ее список по прежднему там.

        # удовлетворенная, она снова ложится спать

    def test_multiple_users_can_start_list_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить павлиньи перья')

        # Она замечает что ее список имеет уникальный адресс
        edth_list_url = self.browser.current_url
        self.assertRegex(edth_list_url, '/lists/.+')

        # Приходит новый пользователь Френсис
        # Хотел ввести свой список
        # Мы используем новый сеанс браузер чтобы никакай информацию Эдит не вылезала через куки
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Френсис посещает домашнюю страницу, нет никаких следов списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Френсис начинает новый список, он менее инетерсен чем эдит
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить молоко')

        # Френсис получает уникальный урл адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edth_list_url)

        # Проверяем нет ли следов от списка Эдит в списке Френсиса
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        # Удовлетворенные они оба идут дрыхнуть
        