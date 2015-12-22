from django.core.urlresolvers import reverse
from django.core import mail
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.contrib.sites.models import Site

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
    update_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.title, self.text)

    def get_absolute_url(self):
        return reverse('questions:details', kwargs={'pk': self.id})

    class Meta:
        ordering = ('-pub_date',)


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

    class Meta:
        ordering = ('-pub_date',)

    def save(self, *args, **kwargs):
        ret = super(Answer, self).save(*args, **kwargs)
        if self.question.author.email_notifications:
            body = ("%(author)s answered your question:\n"
                    "Check out his response on our site: %(url)s\n"
                    )
            url = "http://%s%s" % (Site.objects.get_current().domain,
                                   self.get_absolute_url())
            body = _(body) % {'url': url,
                              'author': self.author}
            msg = mail.EmailMessage(
                _("Your question was answered"),
                body,
                to=[self.question.author.email]
                )
            msg.send()
        return ret


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
