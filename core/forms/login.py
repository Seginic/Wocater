from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(max_length=16)
    password = forms.CharField(max_length=20)
    remember_me = forms.BooleanField(required=False)
