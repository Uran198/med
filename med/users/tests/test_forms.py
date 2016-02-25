from django.test import mock

from test_plus import TestCase

from ..forms import SignupForm
from med.users.models import User


class SignupFormTest(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.form_cls = SignupForm
        self.request = mock.Mock()

    def test_singup(self):
        self.assertEqual(len(User.objects.all()), 1)
        user = User.objects.first()
        self.assertEqual(user.is_doctor, False)
        form = self.form_cls({'is_doctor': True})
        self.assertEqual(form.is_valid(), True)
        form.signup(self.request, user)
        user.refresh_from_db()
        self.assertEqual(user.is_doctor, True)
