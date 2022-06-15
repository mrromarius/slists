from cgitb import text
from django.forms import ValidationError
from lists.models import Item, List
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class ItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_default_text(self):
        '''тест заданного по умолчанию текста'''
        item = Item()
        self.assertEqual(item.text, '')

class ListModelTest(TestCase):
    '''тест модели списка'''

    def test_item_is_relates_to_list(self):
        '''тест: элемент связан со списком'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_get_absolute_url(self):
        '''тест: получен абсолютный УРЛ'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_item_are_invelid(self):
        '''тест: повторы элементов не допустимы'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_defferent_lists(self):
        '''тест: Может сохранить тот же элемент в списки'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()

    def test_list_ordering(self):
        '''тест упорядоченного списка'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_represetation(self):
        '''тест строкого представления'''
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
