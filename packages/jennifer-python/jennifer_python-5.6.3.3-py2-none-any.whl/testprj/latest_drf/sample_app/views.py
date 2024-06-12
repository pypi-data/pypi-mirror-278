from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
import datetime
from django.http import HttpResponse


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def unit_test(request):
    from .mytest import all_test
    print('django.views.unit_test', 'called', datetime.datetime.now())
    return HttpResponse(all_test())
