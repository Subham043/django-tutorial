from rest_framework import serializers
from django import forms
from .models import Article
from django.contrib.auth.models import User

ARTICLE_FOR_CHOICES = [
    ('FOR_KIDS', 'Kids'),
    ('FOR_ADULTS', 'Adults'),  
]

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    slug = serializers.CharField(max_length=100, allow_blank=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    article_for = serializers.ChoiceField(choices=ARTICLE_FOR_CHOICES, default='Adults')
    is_draft = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.is_draft = validated_data.get('is_draft', instance.is_draft)
        instance.save()
        return instance
    
class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'articles']