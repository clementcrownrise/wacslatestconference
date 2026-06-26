from django import forms
from accounts.models import Account
from .models import Confregdetail
from  faculty.models import Faculty

class ConfregdetailForm(forms.ModelForm):
    class Meta:
        model  = Confregdetail
        exclude = [
             'user',
             'conferencename',
        ]

        widgets = {
            'institutionName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Institution Name'
            }),
            'conferencename': forms.Select(attrs={
                'class': 'form-select'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-select'
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subspecialty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'accompany': forms.Select(attrs={
                'class': 'form-select'
            }),
            'wacsfellow': forms.Select(attrs={
                'class': 'form-select'
            }),
            'registration_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'user': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

