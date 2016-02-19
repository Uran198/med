from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('questions:list')
        return super(TemplateView, self).dispatch(request, *args, **kwargs)


class ThanksView(TemplateView):
    template_name = 'pages/thanks.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("thanks")

    def form_valid(self, form):
        form.send_email()
        return super(FormView, self).form_valid(form)
