from django.core.urlresolvers import reverse
from django.db import models

from autoslug import AutoSlugField

from med.users.models import User


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    slug = AutoSlugField(populate_from='title')
    author = models.ForeignKey(User)

    def __str__(self):
        return "{}: {}".format(self.title, self.text)

    def get_absolute_url(self):
        return reverse('questions:details', kwargs={'pk': self.id})


class Comment(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField()
    parent = models.ForeignKey(Question)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.parent.get_absolute_url()
