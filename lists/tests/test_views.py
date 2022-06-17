from glob import escape
from pickle import DUP
from unittest import skip
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,ItemForm, ExistingListItemForm
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

    def post_invalid_input(self):
        '''отправляет недопустимый ввод'''
        list_ =List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text':''}
        )

    def test_for_invalid_input_renders_list_template(self):
        '''тест на недопустимый ввод: отображается шаблон списка'''
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест на недопустимый ввод: форма передается в шаблон'''
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):
        '''тест на недопустимый ввод: на странице отоброжается ошибка'''
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_display_item_form(self):
        '''тест отображения формы для элемента'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        '''тест: ошибки валидации повторяющегося элемента
        оканчиваются на странице списков'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        response = self.client.post(f"/lists/{list1.id}/", data={"text": "textey"})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)

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

    def test_for_invalid_input_renders_home_template(self):
        '''тест на допустимый ввод: отоброжает домашний шаблон'''
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_validation_errors_are_show_on_home_page(self):
        '''тест ошибки валидации выподятся на домашней странице'''
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест на недопустимый ввод: форма передается в шаблон'''
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_item_arent_saved(self):
        '''тест: сохраняются недопустимые элементы списка'''
        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)