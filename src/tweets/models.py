from django.db import models
from django.urls import reverse_lazy, reverse
from django.conf import settings
import re
from django.utils import timezone

from django.db.models.signals import post_save

from hashtags.signals import parsed_hastags


class TweetManager(models.Manager):

    def retweet(self, user, tweet):
        if tweet.parent:
            retweet_parent = tweet.parent
        else:
            retweet_parent = tweet

        qs = self.get_queryset().filter(user=user, parent=retweet_parent).filter(timestamp__year=timezone.now().year, timestamp__month=timezone.now().month, timestamp__day=timezone.now().day)

        if qs.exists():
            return None

        retweet = self.model(parent=retweet_parent, user=user, content=tweet.content)
        retweet.save()

        return retweet



class Tweet(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tweets', on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse_lazy('tweets:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp']


def tweet_post_save_receiver(sender, instance, created, *args, **kwargs):

    user_regex = r'(?P<username>[\w.]+)'
    usernames = re.findall(user_regex, instance.content)
    #send notifications to the users

    hash_regex = r'#(?P<hashtag>[\w-]+)'
    hashtags = re.findall(hash_regex, instance.content)
    #send hashtag signal to the users
    parsed_hastags.send(sender=instance.__class__, hashtag_list=hashtags)


post_save.connect(tweet_post_save_receiver, sender=Tweet)
