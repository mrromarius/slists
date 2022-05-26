from cgitb import text
from glob import escape
from pydoc import doc
from re import I
from telnetlib import DO
from urllib import response
from xml.dom import ValidationErr
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm
from lists.views import home_page


class HomePageTest(TestCase):

    def test_used_home_templates(self):
        '''тест: домашняя страница возвращает правильный html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        '''тест: домашняя страница использует форму для элемента'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_can_save_a_POST_request_to_existing_list(self):
        '''тест: можно сохранять пост-запрос в существующий список'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/', data={'text':'Новый элемент для существующего списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент для существующего списка')
        self.assertEqual(new_item.list, correct_list)


    def test_passes_correct_list_to_template(self):
        '''тест передаем правильный шаблон текста'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_POST_redirects_to_list_view(self):
        '''тест переадресуется в представление списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/', data={'text':'Новый элемент для существующего списка'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        '''тест: ошибки валидации оканчиваются на странице списков'''
        list_ =List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text':''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("Поле не должно быть пустым!")
        self.assertContains(response, expected_error)

class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест:можно сохранить пост запрос'''
        response = self.client.post(
            '/lists/new', data={'text': 'Новый элемент списка'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент списка')

    def test_redirects_after_POST(self):
        '''тест проверяет переадресацию после пост запроса'''
        response = self.client.post('/lists/new', data={'text': 'Новый элемент списка'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_cannot_save_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        '''тест: ошибки валидации отсылают назад в шаблон домашней страницы'''
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = "Поле не должно быть пустым!"
        self.assertContains(response, expected_error)
    
    def test_invalid_list_item_arent_saved(self):
        '''тест: сохраняются недопустимые элементы списка'''
        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)