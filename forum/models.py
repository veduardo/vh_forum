# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from tagging.fields import TagField
from tagging.models import Tag
from tagging.registry import register


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    category = TagField()

    def __str__(self):
        return "%s" % self.title

    def get_tags(self):
        return Tag.objects.get_for_object(self)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User)
    text = models.TextField(blank=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

register(Post)