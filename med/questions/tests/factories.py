import factory

from med.users.models import User
from ..models import Question, Answer, Tag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'johny_{0}'.format(n))
    password = 'password'


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    title = 'Title'
    text = 'Some text'
    author = factory.SubFactory(UserFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    text = "This is Answer"
    question = factory.SubFactory(QuestionFactory)
    author = factory.SubFactory(UserFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: 'tag_{0}'.format(n))
