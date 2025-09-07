from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm,UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = models.CustomUser
        feilds = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationform(AuthenticationForm):
    class Meta:
        model = models.CustomUser
        feilds = ('username', 'email')

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True)

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = models.CustomUser
        feilds = ('new_password1', 'new_password2')

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = models.CustomUser
        feilds = ('username', 'email', 'first_name', 'last_name')

        def  __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.feilds['username'].widget.attrs.update({'class' : 'form-control'})
            self.feilds['email'].widget.attrs.update({'class' : 'form-control'})
            self.feilds['first_name'].widget.attrs.update({'class' : 'form-control'})
            self.feilds['last_name'].widget.attrs.update({'class' : 'form-control'})
