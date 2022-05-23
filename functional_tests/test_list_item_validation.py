import imp
from .base import FunctionalTest
from unittest import skip

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    '''тест валидации элемента списка'''
    
    def test_cannot_add_emnpty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Эдит открывает домашнюю страницу и случаной пытается отправить 
        # постой элемент списка. Она нажимает Энтер на пустом поле воода
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # Домашняя страница обновляется и появлется сообщение об ошибке
        # которое говорит, что элемент списка не должен быть пустым
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Поле не должно быть пустым"
        )) 
        # Она пробует снова, теперь с неким текстом для элемента, и теперь это работает
        self.browser.find_element_by_id('id_new_item').send_keys('Купить молока')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить молока')
        # как ни странно, Эдит решает отправить второй пустой элемент списка
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Она получается аналогичное предупреждение на странице списка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Поле не должно быть пустым"
        ))
        # Она получает аналогичное предупреждение на странице списка
        self.browser.find_element_by_id('id_new_item').send_keys('Получить чаёк')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить молока')
        self.wait_for_row_in_list_tabel('2. Получить чаёк')
        #  И она может его исправить, заполнив поле неким текстом
        