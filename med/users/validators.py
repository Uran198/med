from django.core.exceptions import ValidationError


# TODO: to use custom size not built in should use
# class validators: https://docs.djangoproject.com/en/1.8/ref/validators/
def validate_file_size(f):
    size = 1000000
    if f.size > size:
        raise ValidationError("File too large")
