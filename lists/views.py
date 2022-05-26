from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html', {'form':ItemForm()})

def view_list(request, list_id):
    '''представление списка'''
    list_ =List.objects.get(id=list_id)
    error = None
    
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "Поле не должно быть пустым!"
    return render(request, 'list.html', {'list':list_, 'error':error})

def new_list(request):
    '''создание нового списка'''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "Поле не должно быть пустым!"
        return render(request, 'home.html', {"error":error})
    return redirect(list_)