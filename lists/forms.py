from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "Поле не должно быть пустым!"

class ItemForm(forms.models.ModelForm):
    '''форма элемента списка'''

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
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