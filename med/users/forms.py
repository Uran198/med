from django import forms
from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):
    is_doctor = forms.BooleanField(label=_("I'm a medical specialist"))

    def signup(self, request, user):
        user.is_doctor = self.cleaned_data['is_doctor']
        return user.save()
