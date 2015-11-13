from django.test import TestCase

from med.users.models import User
from ..models import Question


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


class CommentModelTest(TestCase):

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
