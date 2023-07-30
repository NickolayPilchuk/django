from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class UserExtended(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20,default=None,null=True)
    surname = models.CharField(max_length=20,default=None,null=True)
    description = models.TextField(default=None,null=True)
    userpic = models.ImageField(upload_to='userpics',default=None, null=True, blank=True)
    def __str__(self):
        return self.surname


class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    ctime = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='photos', default=None, null=True, blank=True)
    def __str__(self):
        return self.name

class News(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='photos',default=None,null=True,blank=True)
    def __str__(self):
        return self.title


class Comments(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='photos',default=None,null=True,blank=True)