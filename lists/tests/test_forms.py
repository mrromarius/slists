from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item

class ItemFormTest(TestCase):
    '''тест формы элемента списка'''

    def test_form_item_input_has_placeholder_and_css_classes(self):
        '''тест: форма отображает текстовое поле ввода'''
        form = ItemForm()
        self.assertIn('placeholder="Введите элемент списка"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_validation_for_blanck_items(self):
        '''тест: валидация для пустого элемента'''
        form=ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_ITEM_ERROR])