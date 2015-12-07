from django.test import TestCase

from .factories import QuestionFactory, AnswerFactory, TagFactory
from ..models import Question


class TagModelTest(TestCase):

    def setUp(self):
        self.tag = TagFactory.create()

    def test_str(self):
        self.assertEqual(str(self.tag), 'tag_0')


class QuestionModelTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory.create()

    def test_str(self):
        self.assertEqual(str(self.question), "Title: Some text")

    def test_ordering(self):
        question2 = QuestionFactory.create()
        all_question = Question.objects.all()
        self.assertEqual(all_question[0], question2)
        self.assertEqual(all_question[1], self.question)


class AnswerModelTest(TestCase):

    def setUp(self):
        self.question = QuestionFactory()
        self.answer = AnswerFactory.create(question=self.question)

    def test_str(self):
        self.assertEqual(str(self.answer), "This is Answer")

    def test_get_absolute_url(self):
        self.assertEqual(self.answer.get_absolute_url(),
                         self.question.get_absolute_url())

    def test_ordering(self):
        answer2 = AnswerFactory.create(question=self.question)
        all_answers = self.question.answer_set.all()
        self.assertEqual(all_answers[0], answer2)
        self.assertEqual(all_answers[1], self.answer)


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
