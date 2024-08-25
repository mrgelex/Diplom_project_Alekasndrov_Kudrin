from django import forms

class TimeInterval(forms.Form):
    first=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='с')
    last=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='по')