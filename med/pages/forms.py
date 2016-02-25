from django import forms
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"))
    message = forms.CharField(widget=forms.Textarea, label=_("Message"))

    def send_email(self):
        msg = str(self.cleaned_data)
        mail_admins("You got contacted", msg)
