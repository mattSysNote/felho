from django import forms
from .models import Photo
from django.contrib.auth.forms import UserCreationForm

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']

# Regisztrációs űrlap (a beépített Django formot használja alapnak)
class RegistrationForm(UserCreationForm):
    pass