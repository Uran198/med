from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView

from ..mixins import OrderByMixin, UploadImageMixin


class UploadImageMixinText(TestCase):

    def setUp(self):
        class Dummy(UploadImageMixin, TemplateView):
            template_name = "fake.html"
        self.view = Dummy.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake')
        self.response = self.view(self.request)

    def test_get_context_data(self):
        self.assertNotEqual(self.response.context_data.get('image_form'), None)


class OrderByMixinTest(TestCase):

    def setUp(self):
        class Ordering:
            def get_ordering(self):
                return 'ORDERING'

        class Dummy(OrderByMixin, Ordering):
            allowed_order_fields = ['f1', 'f2']
        self.instance = Dummy()
        self.factory = RequestFactory()
        self.instance.request = self.factory.get('/fake?o=f1')

    def test_get_ordering_success(self):
        self.assertListEqual(self.instance.get_ordering(), ['f1'])
        self.instance.request = self.factory.get('/fake?o=-f1')
        self.assertListEqual(self.instance.get_ordering(), ['-f1'])

    def test_get_ordering_fail(self):
        self.instance.request = self.factory.get('/fake?o=unknown')
        self.assertEqual(self.instance.get_ordering(), 'ORDERING')

    def test_allowed_order_fields(self):
        class ImproperlyConfigured(OrderByMixin):
            pass

        instance = ImproperlyConfigured()
        with self.assertRaises(NotImplementedError):
            instance.allowed_order_fields
