from urllib import response
from django.shortcuts import render

def home_page(request):
    '''домашняя страница'''
    return render(response, 'home.html')
