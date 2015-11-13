from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .models import Question


class CreateQuestion(LoginRequiredMixin, CreateView):
    model = Question
    fields = ('title', 'text')

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super(CreateQuestion, self).form_valid(form, *args, **kwargs)


class QuestionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ('title', 'text')

    def test_func(self, user):
        return self.get_object().author == user


class QuestionDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question

    def test_func(self, user):
        return self.get_object().author == user


class QuestionDetails(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context_data = super(QuestionDetails, self).get_context_data()
        context_data['comments'] = self.object.comment_set.all()
        return context_data

    def dispatch(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if question.slug != kwargs.get('slug'):
            kwargs['slug'] = question.slug
            return redirect('questions:details', **kwargs)
        return super(QuestionDetails, self).dispatch(*args, **kwargs)


class QuestionList(ListView):
    model = Question
