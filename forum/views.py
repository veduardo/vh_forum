# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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

def home(request):
    latest_posts = Posts.objects.order_by('-created_on')
    return render(request, 'home.html', { 'latest_posts' : latest_posts })


## Class Based
class PostList(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the comments
        context['comment'] = Comment.objects.all()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy('post_list')
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostView(DetailView):
    model = Post


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy('post_list')
    fields = ['title']


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    success_url = reverse_lazy('post_list')
    fields = ['text']

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)