from rest_framework import generics, permissions

from .serializers import TweetModelSerializer

from tweets.models import Tweet

from django.db.models import Q

from .pagination import StandardPagination


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = Tweet.objects.all().filter(Q(user__in=user.profile.get_following()) | Q(user=user)).order_by('-timestamp')
        q = self.request.GET.get('q', None)
        if q is not None:
            qs = qs.filter(Q(content__icontains=q) | Q(user__username__icontains=q))
        return qs
