from pydoc import doc
from telnetlib import DO
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


class ItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_uses_list_template(self):
        '''тест используется шаблон списка'''
        response = self.client.get('/lists/uniqurl/')
        self.assertTemplateUsed(response, 'list.html')

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получение элементов списка'''
        # FIXME: тет слишком длинный
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

class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_displays_all_items(self):
        '''тест: отоброжаются все элементы в списке'''
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/uniqurl/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест:можно сохранить пост запрос'''
        response = self.client.post(
            '/lists/new', data={'item_text': 'Новый элемент списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент списка')

    def test_redirects_after_POST(self):
        '''тест проверяет переадресацию после пост запроса'''
        response = self.client.post(
            '/lists/new', data={'item_text': 'Новый элемент списка'})
        self.assertRedirects(response, '/lists/uniqurl/')