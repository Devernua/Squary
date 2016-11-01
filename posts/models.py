# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import datetime


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)


class Image(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='posts', blank=True, null=True)
    pdate = models.DateTimeField('date published');

    # rating 	= models.ManyToManyField(User, through='Rating')

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pdate >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Rating(models.Model):
    img = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ForeignKey(Image)
    text = models.CharField(max_length=2000)
    pdate = models.DateTimeField('date published')

    def __str__(self):
        return self.text;

    def was_published_recently(self):
        return self.pdate >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
