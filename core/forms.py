from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import MenuItem


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["category", "name", "price", "stock", "is_available"]


class OrderCreateForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.filter(is_available=True))
    quantity = forms.IntegerField(min_value=1, max_value=20)
    notes = forms.CharField(required=False, max_length=255)


class FeedbackForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    topic = forms.CharField(max_length=120)
    comment = forms.CharField(widget=forms.Textarea)
    would_recommend = forms.BooleanField(required=False)
