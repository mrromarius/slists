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
        self.get_item_input_box().send_keys(Keys.ENTER)

        #Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid')) 

        # Эдит начинает набирать текст нового элемента и ошибка исчезает
        self.get_item_input_box().send_keys('Купить молока')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid')) 

        # И она может отправить его успешно 
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить молока')

        # как ни странно, Эдит решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # И сново браузер не подчиняется
        self.wait_for_row_in_list_tabel('1. Купить молока')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # Она может исправиться, заполнив поле текстом
        self.get_item_input_box().send_keys('Получить чаёк')
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_tabel('1. Купить молока')
        self.wait_for_row_in_list_tabel('2. Получить чаёк')
        