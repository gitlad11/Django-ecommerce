from rest_framework import serializers
from django.contrib.auth import get_user_model

from Users.models import UserProfile
from .models import Comment, Post

User = get_user_model()

#сериалайзеры для представления информации с backend на frontend 
#в формате json 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
       fields =['author', 'text', 'published_on']

class PostSerializer(serializers.ModelSerializer):

    comments_list = CommentSerializer(many=True)
    comments = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ['title', 'body', 'author', 'slug', 'created_on']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'author')

class PostDetailSerializer(serializers.ModelSerializer):
    comments_list = CommentSerializer(many=True)
    total_comments = serializers.IntegerField()
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'author', 'slug', 'created_on']


class  UserProfileSerializer(serializers.ModelSerializer):
    vkontakte_url = serializers.URLField(allow_blank=True, allow_null=True)
    facebook_url = serializers.URLField(allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]

    #создание нового метода update для обновления данных user и Profile c frontend
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        self.update_or_create_profile(instance, profile_data)
        return super(UserProfileSerializer, self).update(instance, validated_data)
    
    def update_create_profile(self, user, profile_data):

        UserProfile.objects.update_profile(user=user, default=profile_data)
        UserProfile.objects.create_profile(user=user, default=profile_data)

#создание формы регистрации на frontend
class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
#стандартные функции создания модели user
    def create(self, validation_data):
        password = validation_data.pop('password')
        user_instance = User.objects.create(**validation_data)
        user_instance.set_password(password)
        user_instance.save()
        #возрашает созданую модель user
        return user_instance