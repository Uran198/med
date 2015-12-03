from django.forms import forms
from django.forms.fields import ImageField
from django.core.exceptions import ValidationError
import django.forms


class UploadImageForm(forms.Form):
    file = ImageField(widget=django.forms.FileInput)

    def clean_file(self):
        cleaned_file = self.cleaned_data['file']
        if cleaned_file:
            if cleaned_file.size > 1*1024*1024:
                raise ValidationError("Image file too large (maximum 1mb)", code='invalid')
            return cleaned_file
        else:
            raise ValidationError("Please choose an image you wish to download!",
                                  code='invalid')
