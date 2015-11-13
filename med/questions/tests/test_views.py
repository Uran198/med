from django.test import TestCase, RequestFactory

from django.contrib.auth.models import AnonymousUser

from med.users.models import User
from ..models import Question
from .. import views


class CreateQuestionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="John",
            password="password"
        )
        self.question = Question.objects.create(
            title="Title",
            text="Some text",
            author=self.user
        )
        self.factory = RequestFactory()
        self.request = self.factory.post('questions/create/',
                                         {'title': 'Title1', 'text': 'Other text'}
                                         )
        self.request.user = self.user
        self.view = views.CreateQuestion.as_view()

    def test_login_required(self):
        self.request.user = AnonymousUser()
        response = self.view(self.request)
        self.assertEqual(response.status_code, 302)
        # TODO: find a better way
        assert 'accounts/login' in response.get('Location')

    def test_form_valid(self):
        response = self.view(self.request)
        self.assertEqual(len(Question.objects.all()), 2)
        self.assertEqual(response.status_code, 302)


class QuestionUpdateTest(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user(
            username="Alice",
            password="secret",
        )
        self.bob = User.objects.create_user(
            username="Bob",
            password="secret",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Text",
            author=self.alice
        )
        self.view = views.QuestionUpdate.as_view()
        self.factory = RequestFactory()

    def test_author_required_success(self):
        request = self.factory.get('questions/update/')
        request.user = self.alice
        response = self.view(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 200)

    def test_author_required_fail(self):
        request = self.factory.get('questions/update/')
        request.user = self.bob
        response = self.view(request, pk=self.question.pk)
        self.assertNotEqual(response.status_code, 200)


class QuestionDeleteTest(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user(
            username="Alice",
            password="secret",
        )
        self.bob = User.objects.create_user(
            username="Bob",
            password="secret",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Text",
            author=self.alice
        )
        self.view = views.QuestionDelete.as_view()
        self.factory = RequestFactory()

    def test_author_required_success(self):
        request = self.factory.get('fake/')
        request.user = self.alice
        response = self.view(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 200)

    def test_author_required_fail(self):
        request = self.factory.get('fake/')
        request.user = self.bob
        response = self.view(request, pk=self.question.pk)
        self.assertNotEqual(response.status_code, 200)


class QuestionDetailsTest(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user(
            username="Alice",
            password="secret",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Text",
            author=self.alice
        )
        self.comment = self.question.comment_set.create(
            text="Comment",
            author=self.alice,
        )
        self.view = views.QuestionDetails.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.get('fake/')

    def test_redirect(self):
        response = self.view(self.request, pk=self.question.pk)
        self.assertEqual(response.status_code, 302)

    def test_no_redirect(self):
        response = self.view(self.request, pk=self.question.pk, slug=self.question.slug)
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        response = self.view(self.request, pk=self.question.pk, slug=self.question.slug)
        self.assertListEqual(list(response.context_data.get('comments')), [self.comment])
