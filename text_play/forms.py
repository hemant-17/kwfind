from django.forms import ModelForm
from django import forms
from .models import *

class UrlForm(ModelForm):
    class Meta:
        model = Url
        fields = '__all__'
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].widget.attrs['placeholder'] = 'https://www.w3schools.com/'
        self.fields['url'].widget.attrs['id'] = 'url'
        self.fields['url'].widget.attrs['name'] = 'url'