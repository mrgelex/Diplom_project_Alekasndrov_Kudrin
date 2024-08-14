from django import forms

class TimeInterval(forms.Form):
    first=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='от')
    last=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='до')