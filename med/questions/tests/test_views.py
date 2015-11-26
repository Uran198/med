from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView

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

    def test_success_delete(self):
        request = self.factory.post('fake/')
        request.user = self.alice
        response = self.view(request, pk=self.question.pk)
        self.assertEqual(response['Location'], reverse('questions:list'))
        self.assertEquals(len(Question.objects.all()), 0)


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


class CommentCreateTest(TestCase):

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
        self.view = views.CommentCreate.as_view()
        self.request = self.factory.post('/fake')
        self.request.user = self.user
        self.request.META['HTTP_REFERER'] = '/'

    def test_allowed_http_methods(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, parent_id=self.question.pk)
        self.assertEqual(response.status_code, 405)

    def test_form_invalid_with_referer(self):
        response = self.view(self.request, parent_id=self.question.pk)
        self.assertEqual(response.status_code, 302)

    def test_form_invalid_no_referer(self):
        request = self.factory.post('/fake')
        request.user = self.user
        response = self.view(request, parent_id=self.question.pk)
        self.assertEqual(response.status_code, 400)

    def test_form_valid(self):
        self.request = self.factory.post('/fake', {'text': 'some text'})
        self.request.META['HTTP_REFERER'] = '/'
        self.request.user = self.user
        self.view(self.request, parent_id=self.question.pk)
        self.assertEqual(len(self.question.comment_set.all()), 1)


class CommentUpdateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="John",
            password="password"
        )
        self.bob = User.objects.create_user(
            username="Bob",
            password="password",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Some text",
            author=self.user
        )
        self.comment = self.question.comment_set.create(
            text="Some comment",
            author=self.user,
        )
        self.factory = RequestFactory()
        self.view = views.CommentUpdate.as_view()
        self.request = self.factory.post('/fake', {'text': "another text"})
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = self.bob
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_author(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 200)

    def test_success_update(self):
        response = self.view(self.request, pk=self.comment.pk)
        self.assertEqual(response['Location'], self.question.get_absolute_url())
        self.assertEqual(self.question.comment_set.get(pk=self.comment.pk).text,
                         "another text")


class CommentDeleteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="John",
            password="password"
        )
        self.bob = User.objects.create_user(
            username="Bob",
            password="password",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Some text",
            author=self.user
        )
        self.comment = self.question.comment_set.create(
            text="Some comment",
            author=self.user,
        )
        self.factory = RequestFactory()
        self.view = views.CommentDelete.as_view()
        self.request = self.factory.post('/fake')
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = self.bob
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_author(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 200)

    def test_success_delete(self):
        response = self.view(self.request, pk=self.comment.pk)
        self.assertEqual(response['Location'], self.question.get_absolute_url())
        self.assertEquals(len(self.question.comment_set.all()), 0)


class UploadImageMixinText(TestCase):

    def setUp(self):
        class Dummy(views.UploadImageMixin, TemplateView):
            template_name = "fake.html"
        self.view = Dummy.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake')
        self.response = self.view(self.request)

    def test_get_context_data(self):
        self.assertNotEqual(self.response.context_data.get('image_form'), None)


class RevisionListTest(TestCase):

    def setUp(self):
        self.skipTest(reason="middleware is disable, don't know how to test")

        self.user = User.objects.create_user("john")
        self.question = Question.objects.create(
            title="Title",
            text="Text",
            author=self.user,
        )
        self.view = views.RevisionList.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake')
        self.request.user = AnonymousUser()

    def test_get_context_data(self):
        response = self.view(self.request, question_pk=self.question.pk)
        self.assertEqual(len(response.context_data['revision_list']), 0)

    def test_get_context_data_revisions_1(self):
        self.question.text = "New text!"
        self.question.save()
        response = self.view(self.request, question_pk=self.question.pk)
        self.assertEqual(len(response.context_data['revision_list']), 1)
