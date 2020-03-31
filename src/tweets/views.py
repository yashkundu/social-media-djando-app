from django.shortcuts import render

from .models import Tweet

from django.views.generic import DetailView, ListView, CreateView, UpdateView,DeleteView

from .forms import TweetForm
from .mixins import UserAttachedMixin, UserNeededMixin

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin


class TweetDetailView(DetailView):
    model = Tweet


class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet


class TweetCreateView(LoginRequiredMixin, UserAttachedMixin, CreateView):
    form_class = TweetForm
    template_name = 'tweets/tweet_create.html'


class TweetUpdateView(LoginRequiredMixin, UserNeededMixin, UpdateView):
    form_class = TweetForm
    template_name = 'tweets/tweet_update.html'
    queryset = Tweet.objects.all()
    

class TweetDeleteView(LoginRequiredMixin, UserNeededMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/tweet_confirm_delete.html'
    success_url = reverse_lazy('home')
