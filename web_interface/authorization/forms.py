from django import forms

class Loginform(forms.Form):
    login=forms.CharField(strip=True, label='Логин')
    password=forms.CharField(strip=True, label='Пароль', widget=forms.PasswordInput())