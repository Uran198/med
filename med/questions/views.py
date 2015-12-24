from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.db.models import F
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView)

from braces.views import LoginRequiredMixin, UserPassesTestMixin
import reversion as revisions

from .models import Question, QuestionComment, Answer, AnswerComment, Tag
from .mixins import OrderByMixin, UploadImageMixin


class CreateQuestion(LoginRequiredMixin, UploadImageMixin, CreateView):
    model = Question
    fields = ('title', 'text', 'tags')

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super(CreateQuestion, self).form_valid(form, *args, **kwargs)


class QuestionUpdate(LoginRequiredMixin, UserPassesTestMixin, UploadImageMixin, UpdateView):
    model = Question
    fields = ('title', 'text')

    def test_func(self, user):
        return self.get_object().author == user

    def form_valid(self, form):
        form.instance.update_date = now()
        return super(QuestionUpdate, self).form_valid(form)


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
        context_data['answers'] = self.object.answer_set.prefetch_related('comment_set').all()
        context_data['tags'] = self.object.tags.all()
        return context_data

    def get(self, *args, **kwargs):
        ret = super(QuestionDetails, self).get(*args, **kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        return ret

    def dispatch(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if question.slug != kwargs.get('slug'):
            kwargs['slug'] = question.slug
            return redirect('questions:details', **kwargs)
        return super(QuestionDetails, self).dispatch(*args, **kwargs)


class QuestionClose(UserPassesTestMixin, UpdateView):
    http_method_names = [u'post']
    model = Question
    fields = ('is_closed',)

    def test_func(self, user):
        return self.get_object().author == user


class QuestionAskedList(LoginRequiredMixin, OrderByMixin, ListView):
    paginate_by = 10
    model = Question
    allowed_order_fields = ['answers', 'views', 'pub_date']
    queryset = Question.objects.annotate(answers=Count('answer'))

    def get_queryset(self):
        qs = super(QuestionAskedList, self).get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs


class QuestionArchiveList(OrderByMixin, ListView):
    paginate_by = 10
    model = Question
    queryset = Question.objects.filter(is_closed=True).annotate(answers=Count('answer'))
    allowed_order_fields = ['answers', 'views', 'pub_date']


class QuestionList(OrderByMixin, ListView):
    paginate_by = 10
    model = Question
    queryset = Question.objects.filter(is_closed=False).annotate(answers=Count('answer'))
    allowed_order_fields = ['answers', 'views', 'pub_date']


class RevisionList(TemplateView):
    template_name = "questions/revision_list.html"

    def get_context_data(self, **kwargs):
        obj = get_object_or_404(Question, pk=kwargs.get('question_pk'))
        context_data = super(RevisionList, self).get_context_data()
        context_data['revision_list'] = [x.object_version.object for x in revisions.get_for_object(obj)]
        return context_data


class AnswerRevisionList(TemplateView):
    template_name = "questions/revision_list.html"

    def get_context_data(self, **kwargs):
        obj = get_object_or_404(Answer, pk=kwargs.get('answer_pk'))
        context_data = super(AnswerRevisionList, self).get_context_data()
        context_data['revision_list'] = [x.object_version.object for x in revisions.get_for_object(obj)]
        return context_data


class AnswerCreate(LoginRequiredMixin, UserPassesTestMixin, UploadImageMixin, CreateView):
    model = Answer
    fields = ('text',)

    def test_func(self, user):
        return user.has_perm('questions.add_answer')

    def post(self, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=kwargs['parent_id'])
        return super(AnswerCreate, self).post(*args, **kwargs)

    def form_valid(self, form):
        form.instance.question = self.question
        form.instance.author = self.request.user
        return super(AnswerCreate, self).form_valid(form)


class AnswerUpdate(LoginRequiredMixin, UserPassesTestMixin, UploadImageMixin, UpdateView):
    model = Answer
    fields = ('text',)

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class AnswerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class CommentCreate(LoginRequiredMixin, CreateView):
    http_method_names = [u'post']
    fields = ('text',)

    def post(self, *args, **kwargs):
        self.parent = get_object_or_404(self.parent_model, pk=kwargs['parent_id'])
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
    template_name = 'questions/comment_form.html'
    fields = ('text',)

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'questions/comment_confirm_delete.html'

    def test_func(self, user):
        return self.get_object().author == user

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class QuestionCommentCreate(CommentCreate):
    parent_model = Question
    model = QuestionComment


class QuestionCommentUpdate(CommentUpdate):
    model = QuestionComment


class QuestionCommentDelete(CommentDelete):
    model = QuestionComment


class AnswerCommentCreate(CommentCreate):
    parent_model = Answer
    model = AnswerComment


class AnswerCommentUpdate(CommentUpdate):
    model = AnswerComment


class AnswerCommentDelete(CommentDelete):
    model = AnswerComment


class TagList(ListView):
    model = Tag
    http_method_names = [u'get']


class TagDetail(DetailView):
    model = Tag
    http_method_names = [u'get']

    def get_context_data(self, **kwargs):
        context_data = super(TagDetail, self).get_context_data(**kwargs)
        context_data['questions'] = self.object.question_set.order_by('-pub_date')
        return context_data
