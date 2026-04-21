from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Tip

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class SignInForm(AuthenticationForm):
    class Meta:
        model = User

class CreateTipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["content"]
        labels = {"content": "Share your tips !"}