from blog.models import *
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    # articles = serializers.HyperlinkedIdentityField(view_name='userpost-list', lookup_field='username')
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = Author
        fields = ('id', 'username', 'url')


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    # photos = serializers.HyperlinkedIdentityField(view_name='postphoto-list')
    # author = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username')

    def get_validation_exclusions(self):
        # Need to exclude `author` since we'll add that later based off the request
        exclusions = super(ArticleSerializer, self).get_validation_exclusions()
        return exclusions + ['author']

    class Meta:
        model = Article
