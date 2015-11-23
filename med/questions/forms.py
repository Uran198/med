from django.forms import forms
from django.forms.fields import ImageField


class UploadImageForm(forms.Form):
    file = ImageField()
