from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import CustomUser


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class AccountRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'wallet_initials',     # додано
            'wallet_address',      # додано
            'password1',
            'password2',
        )



class ProfileForm(UserChangeForm):
    password = None
    new_password = forms.CharField(required=False, label="Новий пароль")

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone',
            'wallet_initials',     # додано
            'wallet_address',      # додано
            'new_password',
        )