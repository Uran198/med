from django.core.urlresolvers import reverse
from django.db import models

from autoslug import AutoSlugField
import reversion as revisions

from med.users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


@revisions.register
class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    slug = AutoSlugField(populate_from='title')
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return "{}: {}".format(self.title, self.text)

    def get_absolute_url(self):
        return reverse('questions:details', kwargs={'pk': self.id})


@revisions.register
class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.question.get_absolute_url()

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.parent.get_absolute_url()

    class Meta:
        abstract = True


class QuestionComment(Comment):
    parent = models.ForeignKey(Question, related_name='comment_set')


class AnswerComment(Comment):
    parent = models.ForeignKey(Answer, related_name='comment_set')
