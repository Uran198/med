from test_plus import TestCase
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

from ..validators import validate_file_size


class TestFileValidation(TestCase):

    def test_valid_file_size(self):
        f = UploadedFile(size=1000000)
        try:
            validate_file_size(f)
        except ValidationError:
            self.fail("validate_file_size raised ValidationError unexpectedly!")

    def test_invalid_file_size(self):
        f = UploadedFile(size=1000001)
        self.assertRaises(ValidationError, validate_file_size, f)
