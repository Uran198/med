from django.forms import forms
from django.forms.fields import ImageField
from django.core.exceptions import ValidationError
from django.core.files.storage import get_storage_class
import django.forms


# TODO: should this form live in api or api's view should live in questions views
class UploadImageForm(forms.Form):
    file = ImageField(widget=django.forms.FileInput)

    def clean_file(self):
        cleaned_file = self.cleaned_data['file']
        # # TODO: Maybe use logging for such purposes
        # print("here")
        # from django.core.files.images import get_image_dimensions
        # w, h = get_image_dimensions(cleaned_file)
        # print(w, h)
        if cleaned_file.size > 1*1024*1024:
            raise ValidationError("Image file too large (maximum 1mb)", code='invalid')
        return cleaned_file

    def save(self):
        storage = get_storage_class()()
        f = self.cleaned_data['file']
        filename = storage.get_available_name(f.name)
        with storage.open(filename, 'wb') as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        self.file_url = storage.url(filename)
