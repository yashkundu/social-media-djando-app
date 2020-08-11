from django.shortcuts import render

from django.views import View

from .models import HashTag


class HashTagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        hashtag, created = HashTag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_view.html', {'hashtag':hashtag})
