from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

#передача свойств в обьект для показа несколько или всех коментариев
#property = self.comments как свойство этого класса
    @property
    def comments(self):
        return self.comments.filter(displayed=True)

    @property
    def total_comments(self):
        return self.comments_list.count()

#вызов slug генератора сигналом после создания поста

class Comment(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} , {self.post}'
