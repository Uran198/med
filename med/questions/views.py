from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.forms import modelform_factory

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .models import Question, Comment


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

    def get_success_url(self):
        return reverse('questions:list')


class QuestionDetails(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context_data = super(QuestionDetails, self).get_context_data()
        context_data['comments'] = self.object.comment_set.all()
        # TODO: This must be wrong!
        context_data['comment_form'] = modelform_factory(CommentCreate.model,
                                                         fields=CommentCreate.fields)()
        return context_data

    def dispatch(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if question.slug != kwargs.get('slug'):
            kwargs['slug'] = question.slug
            return redirect('questions:details', **kwargs)
        return super(QuestionDetails, self).dispatch(*args, **kwargs)


class QuestionList(ListView):
    model = Question


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = [u'post']
    fields = ('text',)

    def post(self, *args, **kwargs):
        self.parent = get_object_or_404(Question, pk=kwargs['parent_id'])
        return super(CommentCreate, self).post(*args, **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.parent
        form.instance.author = self.request.user
        return super(CommentCreate, self).form_valid(form)

    def form_invalid(self, form):
        referer = self.request.META.get('HTTP_REFERER')
        if not referer:
            return HttpResponseBadRequest()
        return redirect(referer)


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('text',)

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        # Strange: it's no lpnger in database, but it is here, and can access
        # foreighn keys
        return self.get_object().get_absolute_url()
