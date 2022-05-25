from tkinter import CASCADE
from django.db import models
from django.urls import reverse

class List(models.Model):
    '''списки'''
    def get_absolute_url(self):
        '''получить абсолютный урл'''
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    ''''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
