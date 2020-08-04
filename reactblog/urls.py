from django.urls import path

from .views import *

urlpatterns = [
    path('posts', PostListView.as_view()),
    path('post/<slug>', PostDetailView.as_view()),
    path('comments', comment_list_view),
    path('create/<slug>', comment_create_view),
    path('register/', UserSignUpview.as_view())
    ]