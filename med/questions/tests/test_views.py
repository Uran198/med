from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView

from django.contrib.auth.models import AnonymousUser, Permission

from .factories import AnswerFactory, QuestionFactory, UserFactory, TagFactory
from ..models import Question, QuestionComment
from .. import views


class CreateQuestionTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.user = self.question.author
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
        self.alice = UserFactory()
        self.bob = UserFactory()
        self.question = QuestionFactory(author=self.alice)
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

    def test_update_field(self):
        request = self.factory.post('/fake', {'title': "New_title",
                                              'text': self.question.text})
        request.user = self.alice
        response = self.view(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        before_date = self.question.update_date
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, 'New_title')
        self.assertNotEqual(self.question.update_date, before_date)


class QuestionArchiveListTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.question_closed = QuestionFactory(is_closed=True)
        self.view = views.QuestionArchiveList()

    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        self.assertEqual(queryset[0].answers, 0)
        self.assertSequenceEqual(queryset, [self.question_closed])


class QuestionListTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.question_closed = QuestionFactory(is_closed=True)
        self.view = views.QuestionList()

    def test_get_queryset(self):
        queryset = self.view.get_queryset()
        self.assertEqual(queryset[0].answers, 0)
        self.assertSequenceEqual(queryset, [self.question])


class QuestionDeleteTest(TestCase):

    def setUp(self):
        self.alice = UserFactory()
        self.bob = UserFactory()
        self.question = QuestionFactory(author=self.alice)
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
        self.question = QuestionFactory()
        self.tag = self.question.tags.create(name='tag0')
        self.comment = self.question.comment_set.create(
            text="Comment",
            author=self.question.author,
        )
        self.answer = AnswerFactory(question=self.question)
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
        self.assertListEqual(list(response.context_data.get('answers')), [self.answer])
        self.assertListEqual(list(response.context_data.get('tags')), [self.tag])

    def test_get(self):
        self.assertEqual(self.question.views, 0)
        self.view(self.request, pk=self.question.pk, slug=self.question.slug)
        self.question.refresh_from_db()
        self.assertEqual(self.question.views, 1)

    def test_no_update_on_view(self):
        before = self.question.update_date
        self.view(self.request, pk=self.question.pk, slug=self.question.slug)
        self.question.refresh_from_db()
        self.assertEqual(self.question.update_date, before)


class QuestionCloseTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.user = self.question.author
        self.bob = UserFactory()
        self.view = views.QuestionClose.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.post('fake/', {'is_closed': True})
        self.request.user = self.user

    def test_get(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 405)

    def test_is_not_author(self):
        self.request.user = self.bob
        self.view(self.request, pk=self.question.pk)
        self.question.refresh_from_db()
        self.assertEqual(self.question.is_closed, False)

    def test_success_close(self):
        response = self.view(self.request, pk=self.question.pk)
        self.assertEqual(response['Location'], self.question.get_absolute_url())
        self.question.refresh_from_db()
        self.assertEqual(self.question.is_closed, True)


class AnswerCreateTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.user = self.question.author
        self.add_answer_permission = Permission.objects.get(codename='add_answer', content_type__app_label='questions')
        self.user.user_permissions.add(self.add_answer_permission)
        self.factory = RequestFactory()
        self.view = views.AnswerCreate.as_view()
        self.request = self.factory.post('/fake')
        self.request.user = self.user

    def test_login_required(self):
        request = self.factory.post('/fake', {'text': 'some text'})
        request.user = AnonymousUser()
        response = self.view(request, parent_id=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.question.answer_set.all()), 0)

    def test_user_cannot_answer(self):
        request = self.factory.post('/fake', {'text': 'some text'})
        request.user = self.user
        self.user.user_permissions.remove(self.add_answer_permission)
        self.view(request, parent_id=self.question.pk)
        self.assertEqual(len(self.question.answer_set.all()), 0)

    def test_form_invalid(self):
        response = self.view(self.request, parent_id=self.question.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.question.answer_set.all()), 0)

    def test_form_valid(self):
        self.request = self.factory.post('/fake', {'text': 'some text'})
        self.request.user = self.user
        self.view(self.request, parent_id=self.question.pk)
        self.assertEqual(len(self.question.answer_set.all()), 1)


class AnswerUpdateTest(TestCase):

    def setUp(self):
        self.answer = AnswerFactory()
        self.user = self.answer.author
        self.question = self.answer.question
        self.factory = RequestFactory()
        self.view = views.AnswerUpdate.as_view()
        self.request = self.factory.post('/fake', {'text': "another text"})
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = UserFactory()
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_author(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 200)

    def test_success_update(self):
        response = self.view(self.request, pk=self.answer.pk)
        self.assertEqual(response['Location'], self.question.get_absolute_url())
        self.assertEqual(self.question.answer_set.get(pk=self.answer.pk).text,
                         "another text")


class AnswerDeleteTest(TestCase):

    def setUp(self):
        self.answer = AnswerFactory()
        self.user = self.answer.author
        self.question = self.answer.question
        self.factory = RequestFactory()
        self.view = views.AnswerDelete.as_view()
        self.request = self.factory.post('/fake')
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = UserFactory()
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_author(self):
        request = self.factory.get('/fake')
        request.user = self.user
        response = self.view(request, pk=self.answer.pk)
        self.assertEqual(response.status_code, 200)

    def test_success_delete(self):
        response = self.view(self.request, pk=self.answer.pk)
        self.assertEqual(response['Location'], self.question.get_absolute_url())
        self.assertEquals(len(self.question.answer_set.all()), 0)


class CommentCreateTest(TestCase):

    def setUp(self):
        class Dummy(views.CommentCreate):
            model = QuestionComment
            parent_model = Question
        self.question = QuestionFactory()
        self.user = self.question.author
        self.factory = RequestFactory()
        self.view = Dummy.as_view()
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
        class Dummy(views.CommentUpdate):
            model = QuestionComment
        self.question = QuestionFactory()
        self.user = self.question.author
        self.comment = self.question.comment_set.create(
            text="Some comment",
            author=self.user,
        )
        self.factory = RequestFactory()
        self.view = Dummy.as_view()
        self.request = self.factory.post('/fake', {'text': "another text"})
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = UserFactory()
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
        class Dummy(views.CommentDelete):
            model = QuestionComment
        self.question = QuestionFactory()
        self.user = self.question.author
        self.comment = self.question.comment_set.create(
            text="Some comment",
            author=self.user,
        )
        self.factory = RequestFactory()
        self.view = Dummy.as_view()
        self.request = self.factory.post('/fake')
        self.request.user = self.user

    def test_anonymous(self):
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request, pk=self.comment.pk)
        self.assertEqual(response.status_code, 302)

    def test_is_not_author(self):
        request = self.factory.get('/fake')
        request.user = UserFactory()
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
        self.skipTest(reason="middleware is disabled, don't know how to test")

        self.question = QuestionFactory()
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


class AnswerRevisionListTest(TestCase):

    def setUp(self):
        self.skipTest(reason="middleware is disabled, don't know how to test")

        self.answer = AnswerFactory(text="Answer")
        self.view = views.AnswerRevisionList.as_view()
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake')
        self.request.user = AnonymousUser()

    def test_get_context_data(self):
        response = self.view(self.request, answer_pk=self.answer.pk)
        self.assertEqual(len(response.context_data['revision_list']), 0)

    def test_get_context_data_revisions_1(self):
        self.answer.text = "New text!"
        self.answer.save()
        response = self.view(self.request, answer_pk=self.answer.pk)
        self.assertEqual(len(response.context_data['revision_list']), 1)


class TagListTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = views.TagList.as_view()

    def test_post(self):
        request = self.factory.post('/fake')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_context_data(self):
        tags = TagFactory.create_batch(3)
        request = self.factory.get('/fake')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertListEqual(list(response.context_data['object_list']), tags)


class TagDetailTest(TestCase):

    def setUp(self):
        self.tag = TagFactory.create()
        self.untagged_question = QuestionFactory.create()
        self.factory = RequestFactory()
        self.view = views.TagDetail.as_view()
        self.request = self.factory.get('/fake')
        self.request.user = AnonymousUser()

    def test_post(self):
        request = self.factory.post('/fake')
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 405)

    def test_no_questions(self):
        response = self.view(self.request, pk=self.tag.pk)
        questions = response.context_data['questions']
        self.assertEqual(len(questions), 0)

    def test_with_questions(self):
        question = QuestionFactory.create()
        question.tags.add(self.tag)
        response = self.view(self.request, pk=self.tag.pk)
        questions = response.context_data['questions']
        self.assertListEqual(list(questions), [question])

    def test_order(self):
        que1 = QuestionFactory.create()
        que1.tags.add(self.tag)
        que2 = QuestionFactory.create()
        que2.tags.add(self.tag)
        response = self.view(self.request, pk=self.tag.pk)
        questions = response.context_data['questions']
        self.assertEqual(questions[0], que2)
        self.assertEqual(questions[1], que1)
