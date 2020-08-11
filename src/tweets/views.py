from django.shortcuts import render, get_object_or_404, redirect

from .models import Tweet

from django.views.generic import DetailView, ListView, CreateView, UpdateView,DeleteView
from django.views import View
from .forms import TweetForm
from .mixins import UserAttachedMixin, UserNeededMixin

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q


class RetweetView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        retweet = Tweet.objects.retweet(request.user, tweet)
        return redirect('/')


class TweetDetailView(DetailView):
    model = Tweet


class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = Tweet.objects.filter(Q(user__in=user.profile.following.all()) | Q(user=user)).distinct().order_by('-timestamp')
        q = self.request.GET.get('q',  None)
        if q is not None:
            qs = qs.filter(Q(content__icontains=q) | Q(user__username__icontains=q))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        context['form'] = TweetForm()
        context['url'] = reverse_lazy('tweets:create')
        return context


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
