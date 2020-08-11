from django.conf.urls import url

from tweets.api.views import TweetListAPIView

app_name = 'accounts-api'

urlpatterns = [
    url(r'^(?P<username>[\w.]+)/tweets/$', TweetListAPIView.as_view(), name='list')
]
