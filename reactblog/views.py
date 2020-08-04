from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, UserSignUpSerializer, PostDetailSerializer
from .models import Post, Comment
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

#лист всех постов на frontend
class PostListView(generics.ListAPIView):
    #queryset, serializer_class обязательные поля 
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

#возрашает данные модели на get запрос
@api_view(['GET'])
def comment_list_view(request, slug):
    post_instance = get_object_or_404(Post, slug=slug)
    comment_list = Comment.objects.filter(post=post_instance)
    serializer_class = CommentSerializer(comment_list, many=True)
    return Response(serializer_class.data)

#принимает post запрос на создание модели коментария в db
@api_view(['POST'])
def comment_create_view(request, slug):
    post_instance = get_object_or_404(Post, slug=slug)
    request.data['post'] = post_instance.pk
    serializer_class = CommentSerializer(data=request.data)
    if serializer_class.is_valid():
        serializer_class.save()
        return Response(serializer_class.data)
    return Response(serializer_class.errors)

#request data приходит в json формате на сериалазер
class UserSignUpview(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    def post(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        password = request.data.get('password1')

        #обычная валидация форм django, только response отправляется на frontend
        if not first_name or email:
            return Response({'detail': 'name and email is required!'})
        elif password != password1 or not password:
            return Response({'detail': 'Password does not matchs'})
        else:
            serializer_class = UserSignUpSerializer(data=request.data)
            if serializer_class.is_valid:
                serializer_class.save()
                User.set_password('password1')
                #возращает на frontend созданые данные
                return Response(serializer_class.data)
