from django.test import TestCase, RequestFactory

from ..mixins import OrderByMixin


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
