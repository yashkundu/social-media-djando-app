from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import FormView, DetailView
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout

from django import forms
from django.views import View

from django.forms.utils import ErrorList
from django.contrib.auth import get_user_model

from .models import UserProfile

from django.contrib.auth.mixins import LoginRequiredMixin


User = get_user_model()

def user_login_view(request):
    form = LoginForm()
    next_url = request.GET.get('next', None)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url is not None:
                    return redirect(next_url)
                return redirect('home')
            else:
                form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User does not exists.'])
    return render(request, 'accounts/user_login.html',{'form': form})


def user_logout_view(request):
    logout(request)
    return redirect('accounts:login')



class UserRegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/user_registration.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)

        return super(UserRegisterView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'accounts/user_detail.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['is_following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
        return context


class UserFollowView(LoginRequiredMixin, View):
    login_url='/accounts/login/'
    def get(self, request, username, *args, **kwargs):
        other_user = get_object_or_404(User, username=username)
        is_following = UserProfile.objects.toggle_follow(request.user, other_user)

        return redirect('accounts:detail', username=username)
