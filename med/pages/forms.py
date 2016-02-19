from django import forms
from django.core.mail import mail_admins


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        msg = str(self.cleaned_data)
        mail_admins("You got contacted", msg)
