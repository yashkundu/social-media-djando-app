from django.db import models

from django.urls import reverse_lazy

from tweets.models import Tweet

from .signals import parsed_hastags

class HashTag(models.Model):
    tag = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '#'+self.tag

    def get_absolute_url(self):
        return reverse_lazy('hashtag', kwargs={'hashtag': self.tag})

    def get_tweets(self):
        return Tweet.objects.filter(content__contains='#'+self.tag)



def parsed_hastags_receiver(sender, hashtag_list, *args, **kwargs):
    if len(hashtag_list)>0:
        for tag in hashtag_list:
            hashtag, created = HashTag.objects.get_or_create(tag=tag)



parsed_hastags.connect(parsed_hastags_receiver)
