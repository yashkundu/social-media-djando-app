from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TweetModelSerializer

from tweets.models import Tweet

from django.db.models import Q

from .pagination import StandardPagination


class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = 'Not Allowed'
        if tweet_qs.exists() and tweet_qs.count()==1:
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
            if new_tweet is not None:
                data = TweetModelSerializer(new_tweet).data
                return Response(data)
            message = 'Cannot retweet the same tweet in one day.'
        return Response({'message': message}, status=400)



class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardPagination

    def get_queryset(self, *args, **kwargs):

        requested_username = self.kwargs.get('username', None)

        if requested_username:
            qs = Tweet.objects.filter(user__username=requested_username).order_by('-timestamp')
        else:
            user = self.request.user
            qs = Tweet.objects.all().filter(Q(user__in=user.profile.get_following()) | Q(user=user)).order_by('-timestamp')


        q = self.request.GET.get('q', None)
        if q is not None:
            qs = qs.filter(Q(content__icontains=q) | Q(user__username__icontains=q))
        return qs
