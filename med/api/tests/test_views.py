import tempfile
from PIL import Image

from django.test import TestCase, RequestFactory
from django.utils import translation

from django.contrib.auth.models import AnonymousUser

from med.users.models import User
from .. import views


class UploadImageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="john",
            password="pass",
        )
        self.view = views.UploadImage.as_view()
        translation.activate('en')

    def test_get(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_login_required(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)

    # TODO: testing form should live in test_forms.py
    def test_without_image(self):
        request = self.factory.post('/fake')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.content, b'{"error": {"file": ["This field is required."]}}')

    def test_form_valid(self):
        im = Image.new("RGBA", size=(100, 100), color=(256, 0, 0))
        f = tempfile.NamedTemporaryFile()
        f.name = 'temp.png'
        im.save(f, format='png')
        # put the carret to the beginning of the file
        f.seek(0)
        request = self.factory.post('/fake', {'name': f.name, 'file': f})
        request.user = self.user
        response = self.view(request)
        self.assertContains(response, "location")

    def test_not_a_image(self):
        f = tempfile.NamedTemporaryFile()
        f.name = 'temp.png'
        f.write(b"Not an image magic numbers")
        f.seek(0)
        request = self.factory.post('/fake', {'name': f.name, 'file': f})
        request.user = self.user
        response = self.view(request)
        self.assertContains(response, "Upload a valid image")

    def test_big_file(self):
        im = Image.new("RGBA", size=(10000, 7000), color=(256, 0, 0))
        f = tempfile.NamedTemporaryFile()
        f.name = 'temp.png'
        im.save(f, format='jpeg')
        # put the carret to the beginning of the file
        f.seek(0)
        request = self.factory.post('/fake', {'name': f.name, 'file': f})
        request.user = self.user
        response = self.view(request)
        self.assertContains(response, "Image file too large")
