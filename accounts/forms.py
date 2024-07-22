from django import forms
from django.contrib.auth import authenticate, login
from django.forms import ValidationError
from accounts.models import Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={"class": "login__input", "placeholder": "Username"}))
    password = forms.CharField(max_length=10,
                               widget=forms.PasswordInput(attrs={"class": "login__input", "placeholder": "Password"}))

    def clean_password(self):
        user = authenticate(username=self.cleaned_data.get("username"), password=self.cleaned_data.get("password"))
        if user is not None:
            return self.cleaned_data["password"]
        else:
            raise ValidationError("username and password are wrong", code="invalid_info")


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "login__input", "placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "login__input", "placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "login__input", "placeholder": "Password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login__input", "placeholder": "Repeat password"}))

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("password's are not same", code="invalid_password")


class UserEdirForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ("username", "first_name", "last_name", "email")
