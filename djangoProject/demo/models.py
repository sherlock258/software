from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    phone=models.CharField(max_length=15)
    email=models.CharField(max_length=30,unique = True)
    avatarurl=models.CharField(max_length=1000,default='')
    description=models.CharField(max_length=1000,default='这位博主有点懒，还没有写个人介绍哦 ~')
    def __str__(self):
        return self.username

class Article(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    author=models.ForeignKey(User,models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    count=models.IntegerField(default=0)
    kind=models.IntegerField(default=0)
    html=models.TextField(default='')
    status=models.IntegerField(default=1)
    def print_article(self):
        print(self.__dict__)

class Like(models.Model):
    userid=models.IntegerField(default=0)
    articleid = models.IntegerField(default=0)

class Attention(models.Model):
    liking=models.IntegerField(default=0)
    liked = models.IntegerField(default=0)
    
class Comment(models.Model):
    userid=models.IntegerField(default=0)
    articleid = models.IntegerField(default=0)
    value=models.CharField(max_length=100)
    status= models.IntegerField(default=0)
    towhich=models.CharField(max_length=15,default='')
    time = models.DateTimeField(auto_now_add=True,null=True)


