from pydoc import doc
from re import I
from telnetlib import DO
from urllib import response
from lists.models import Item, List
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


class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получение элементов списка'''
        # FIXME: тет слишком длинный

        list_=List()
        list_.save()

        first_item = Item()
        first_item.text = 'Первый элемент списка'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый элемент списка')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_uses_list_template(self):
        '''тест использования щаблона листов'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        '''тест: отоброжаются все элементы в списке'''
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')

    def test_passes_correct_list_to_template(self):
        '''тест передаем правильный шаблон текста'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

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
        response = self.client.post('/lists/new', data={'item_text': 'Новый элемент списка'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    '''тест нового элемента списка'''

    def test_can_save_a_POST_request_to_existing_list(self):
        '''тест: можно сохранять пост-запрос в существующий список'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text':'Новый элемент для существующего списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент для существующего списка')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        '''тест переадресуется в представление списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text':'Новый элемент для существующего списка'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')