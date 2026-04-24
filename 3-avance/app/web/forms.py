from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Article

User = get_user_model()

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "synopsis",
            "content",
        ]