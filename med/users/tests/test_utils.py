from test_plus.test import TestCase

from ..utils import upload_path


class TestUtils(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_upload_path(self):
        filename = "this_filename.jpg"
        self.assertEqual(upload_path(self.user, filename),
                         "avatars/{pk}.jpg".format(pk=self.user.pk))
