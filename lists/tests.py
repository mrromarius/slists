from urllib import response
from lists.models import Item
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):

    def test_used_home_templates(self):
        '''тест: домашняя страница возвращает правильный html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''тест:можно сохранить пост запрос'''
        response = self.client.post('/', data={'item_text':'Новый элемент списка'})
        self.assertIn('Новый элемент списка', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        
class ItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получение элементов списка'''
        first_item = Item()
        first_item.text = 'Первый элемент списка'
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый элемент списка')
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')