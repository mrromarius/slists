from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "Поле не должно быть пустым!"
DUPLICATE_ITEM_ERROR = "Не повторяйся!!!"


class ItemForm(forms.models.ModelForm):
    '''форма элемента списка'''

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Введите элемент списка',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class ExistingListItemForm(ItemForm):
    '''форма для элемента существующего списка'''

    def __init__(self, for_list, *agrs, **kwargs):
        super().__init__(*agrs, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        '''проверка уникальности'''
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text':[DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
    
    def save(self):
        return forms.models.ModelForm.save(self)