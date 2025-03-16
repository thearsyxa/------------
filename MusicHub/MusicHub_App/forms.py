from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск исполнителя', max_length=100)
