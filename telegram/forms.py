from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your forms here.


class CustomRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-input'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})

    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input'})
        self.fields['password'].widget.attrs.update({'class': 'form-input'})
