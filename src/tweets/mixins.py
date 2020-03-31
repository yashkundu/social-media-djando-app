from django import forms
from django.forms.utils import ErrorList

from django.shortcuts import get_object_or_404
from .models import Tweet

from django.core.exceptions import PermissionDenied

class UserAttachedMixin(object):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super(UserAttachedMixin, self).form_valid(form)
        form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be logged in to continue.'])
        return self.form_invalid(form)


class UserNeededMixin(object):
    def dispatch(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=self.kwargs.get('pk'))
        if tweet.user != request.user:
            raise PermissionDenied('You are not allowed to access it.')
        return super(UserNeededMixin, self).dispatch(request, *args, **kwargs)
