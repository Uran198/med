from django.test import TestCase

from med.users.models import User
from ..models import Question, Answer


class QuestionModelTest(TestCase):

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

    def test_str(self):
        self.assertEqual(str(self.question), "Title: Some text")


class AnswerModelTest(TestCase):

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
        self.answer = Answer.objects.create(
            text="This Is Answer",
            question=self.question,
            author=self.user,
        )

    def test_str(self):
        self.assertEqual(str(self.answer), "This Is Answer")

    def test_get_absolute_url(self):
        self.assertEqual(self.answer.get_absolute_url(),
                         self.question.get_absolute_url())


class QuestionCommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="John",
            password="password",
        )
        self.question = Question.objects.create(
            title="Title",
            text="Some text",
            author=self.user
        )
        self.comment = self.question.comment_set.create(
            author=self.user,
            text='Some comment',
        )

    def test_str(self):
        self.assertEqual(str(self.comment), "Some comment")

    def test_get_absolute_url(self):
        self.assertEqual(self.comment.get_absolute_url(),
                         self.question.get_absolute_url())
