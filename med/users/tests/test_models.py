import tempfile
from PIL import Image

from django.utils import translation
from django.core.files.images import File

from test_plus.test import TestCase


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.prefix = "/" + translation.get_language()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            "testuser"  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            self.prefix + '/users/testuser/'
        )

    def test_save(self):
        im = Image.new("RGBA", size=(500, 500), color=(256, 0, 0))
        f = tempfile.TemporaryFile(suffix=".jpg")
        im.save(f, format="png")
        self.user.avatar = File(f, name="temp.jpg")
        self.user.save()
        self.assertEqual(self.user.avatar.width, 100)
        self.assertEqual(self.user.avatar.height, 100)
