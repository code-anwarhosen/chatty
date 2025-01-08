from django import forms
from django.contrib.auth.forms import AuthenticationForm

tailwindcss_classes_login_form = 'w-full px-4 py-2 mt-1 bg-slate-900 text-white rounded-lg border border-slate-600 focus:ring-2 focus:ring-teal-400 focus:outline-none'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, required=True, label='Username',
        widget=forms.TextInput(attrs={
            'class': tailwindcss_classes_login_form,
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        required=True, label='Password',
        widget=forms.PasswordInput(attrs={
            'class': tailwindcss_classes_login_form,
            'placeholder': '* * * * * * * *'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
