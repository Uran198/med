from django.test import TestCase

from .factories import QuestionFactory, AnswerFactory


class QuestionModelTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory.create()

    def test_str(self):
        self.assertEqual(str(self.question), "Title: Some text")


class AnswerModelTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.answer = AnswerFactory.create(question=self.question)

    def test_str(self):
        self.assertEqual(str(self.answer), "This is Answer")

    def test_get_absolute_url(self):
        self.assertEqual(self.answer.get_absolute_url(),
                         self.question.get_absolute_url())


class QuestionCommentModelTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.comment = self.question.comment_set.create(
            author=self.question.author,
            text='Some comment',
        )

    def test_str(self):
        self.assertEqual(str(self.comment), "Some comment")

    def test_get_absolute_url(self):
        self.assertEqual(self.comment.get_absolute_url(),
                         self.question.get_absolute_url())
