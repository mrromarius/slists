
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10

class NewVisitorTest(FunctionalTest):
    '''тест нового посетителя'''

    def test_can_start_a_list_for_one_user(self):
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Начать новый список задач', header_text)

        # ей сразу же предлагается ввести элемент списка
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        