from django.conf.urls import url

from .views import user_login_view, user_logout_view, UserRegisterView, UserDetailView, UserFollowView



app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', user_login_view, name='login'),
    url(r'^logout/$', user_logout_view, name='logout'),
    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'(?P<username>[\w.]+)/follow/$', UserFollowView.as_view(), name='follow'),
    url(r'(?P<username>[\w.]+)/$', UserDetailView.as_view(), name='detail'),


]
