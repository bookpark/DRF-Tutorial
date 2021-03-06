from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        owner = serializers.ReadOnlyField(
            source='owner.username',
        )
        fields = (
            'id',
            'title',
            'code',
            'linenos',
            'language',
            'style',
            'owner',
        )


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Snippet.objects.all(),
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'snippets',
        )
