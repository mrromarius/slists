from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "Поле не должно быть пустым!"

class ItemForm(forms.models.ModelForm):
    '''форма элемента списка'''

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text':forms.fields.TextInput(attrs={
                'placeholder':'Введите элемент списка',
                'class':'form-control input-lg',
            }),
        }
        error_messages = {
            'text':{'required':EMPTY_ITEM_ERROR}
        }