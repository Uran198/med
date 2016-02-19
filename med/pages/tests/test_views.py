from django.core import mail
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from test_plus.test import TestCase

from .. import views


class HomeViewTest(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
        self.view = views.HomeView.as_view()
        self.request = self.factory.get('fake/')

    def test_user_authenticated(self):
        self.request.user = self.user
        response = self.view(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('Location'), reverse('questions:list'))

    def test_user_not_authenticated(self):
        self.request.user = AnonymousUser()
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)


class ContactViewTest(TestCase):

    def testFormValid(self):
        self.view = views.ContactView.as_view()
        self.request = RequestFactory().post(
            'fake/', {'name': 'ContactName', 'message': 'Message text'})
        self.view(self.request)
        self.assertEqual(len(mail.outbox), 1)
