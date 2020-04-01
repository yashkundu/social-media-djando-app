from django.db import models
from django.conf import settings

from django.db.models.signals import post_save

from django.urls import reverse_lazy

# Create your models here.

class UserProfileManager(models.Manager):

    def all(self):
        qs = self.get_queryset()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, other_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if other_user in user_profile.following.all():
            user_profile.following.remove(other_user)
            is_following = False
        else:
            user_profile.following.add(other_user)
            is_following = True
        return is_following

    def is_following(self, user, other_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if other_user in user_profile.following.all():
            return True
        return False






class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers')

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def get_follow_url(self):
        return reverse_lazy('accounts:follow', kwargs={'username': self.user.username})

    def get_absolute_url(self):
        return reverse_lazy('accounts:detail', kwargs={'username': self.user.username})

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)




def post_save_user_receiver(sender, instance, *args, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
