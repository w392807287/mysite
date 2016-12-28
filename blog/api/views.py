from rest_framework import generics, permissions
from .serializers import AuthorSerializer
from blog.models import Author


class AuthorList(generics.ListCreateAPIView):
    model = Author
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]


class AuthorDetail(generics.RetrieveAPIView):
    model = Author
    serializer_class = AuthorSerializer
    lookup_field = 'username'

    queryset = Author.objects.all()