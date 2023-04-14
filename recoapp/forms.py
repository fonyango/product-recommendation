from django import forms

class MyForm(forms.Form):
    user_id = forms.CharField(max_length=100)
