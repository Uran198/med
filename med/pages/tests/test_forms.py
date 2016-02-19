from django.core import mail

from test_plus import TestCase

from ..forms import ContactForm


class ContactFormTest(TestCase):

    def setUp(self):
        self.message = "Message text"
        self.title = "You got contacted"
        self.name = "John"
        self.form_cls = ContactForm
        self.data = {'name': self.name, 'message': self.message}

    def test_from_valid(self):
        form = self.form_cls(self.data)
        self.assertEqual(form.is_valid(), True)

    def test_send_email(self):
        form = self.form_cls(self.data)
        self.assertEqual(form.is_valid(), True)
        form.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[Django] You got contacted")
        self.assertEqual(mail.outbox[0].body, str(self.data))
