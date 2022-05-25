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

    def test_get_absolute_url(self):
        '''тест: получен абсолютный УРЛ'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
