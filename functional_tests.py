
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
import sys
from sys import platform


class NewVisitorTest(unittest.TestCase):
    '''тест нового посетителя'''
    
    def setUp(self):
        '''установка'''    
        for p in sys.path:
            print(p)   
        if platform == "linux" or platform == "linux2":
    # linux
            print('запуск на Линус')
        elif platform == "darwin":
    # OS X
            print("Запуск на Маке")
            self.browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
        else:
    # Windows...
            print('Запуск на Винде')
            self.browser = webdriver.Firefox()

    def tearDown(self):
        '''уничтожение'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. она решает оценить его домашнюю страницу
        self.browser.get('http://127.0.0.1:8000/')

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Купить павлиньи перья' for row in rows),
            "Новый элемент списка не появился в таблице"
        )
        # текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # она заводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методичка)
        self.fail('Закончить тест!')
        # страница сново обновляется, и теперь показывает оба элемента ее списка

        # Эдит интересно, запомнит ли сайт ее спсико. Далее она видит, что
        # сайт сгенерировал для нее уникальный УРЛ-адрес об этом
        # выводится небольшой текст с объяснениями.

        # она посещяет этот УРЛ адрес- ее список по прежднему там.

        # удовлетворенная, она снова ложится спать
if __name__ == '__main__':
    unittest.main(warnings='ignore')
