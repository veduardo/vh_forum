# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tagging.models import Tag, TaggedItem

from .forms import *
from .models import Post, Comment


## Function Based
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def search_tag(request, tag, object_id=None, page=1):
    try:
        query_tag = Tag.objects.get(name=tag)
    except ObjectDoesNotExist:
        query_tag = ''

    entries = TaggedItem.objects.get_by_model(Post, query_tag)
    return render(request, "forum/tag_list.html", {'tag':tag, 'entries':entries})


## Class Based
class Home(ListView):
    model = Post


class PostList(ListView):
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy('home')
    fields = ['title', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostView(DetailView):
    model = Post


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy('home')
    fields = ['title', 'category']


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    success_url = reverse_lazy('home')
    fields = ['text']

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)