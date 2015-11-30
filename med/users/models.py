# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from PIL import Image

from django.core.urlresolvers import reverse
from django.core.files.images import File
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractUser

from .utils import upload_path
from .validators import validate_file_size


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    avatar = models.ImageField(upload_to=upload_path,
                               blank=True,
                               validators=[validate_file_size])
    can_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    # TODO:
    # remove images from filesystem once they are no longer needed
    def save(self, *args, **kwargs):
        if self.avatar:
            image = Image.open(self.avatar.file)
            wsize = 100
            hsize = int(wsize / image.size[0] * image.size[1])
            image = image.resize((wsize, hsize), Image.ANTIALIAS)
            image.save(self.avatar.path)
            self.avatar = File(open(self.avatar.path, 'rb'))
        return super(User, self).save(*args, **kwargs)
