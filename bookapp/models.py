from typing import Any
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    


class CustomUser(AbstractUser):
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='users/', default='defaults/account.jpg')
    want_to_read = models.ManyToManyField('Book',related_name="want_to_read_users", blank=True)
    currently_reading = models.ManyToManyField('Book',related_name="currently_users", blank=True)
    read = models.ManyToManyField('Book',related_name="read_users", blank=True)

    def __str__(self) -> str:
        return self.username

    @property
    def total_reviews(self):
        return self.review_set.count()



class Author(models.Model):
    name = models.CharField(max_length=100  ,db_index=True)
    about = models.TextField(default="test")
    image = models.ImageField(upload_to='authors/' , null=True)
    followers = models.ManyToManyField(CustomUser)

    def total_followers(self):
        return self.followers.count()

    def __str__(self) -> str:
        return self.name



class Quote(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(Author , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.text[:50]}...'



class Book(models.Model):
    name = models.CharField(max_length=150 , db_index=True)
    cover = models.ImageField(upload_to='covres/')
    about = models.TextField(default='none')
    author = models.ForeignKey(Author , on_delete=models.CASCADE)
    pages = models.IntegerField(default=250)
    genre = models.ManyToManyField(Genre)
    quotes = models.ManyToManyField(Quote ,blank=True)
    published = models.CharField(max_length=10,default="1980")
    created = models.DateTimeField(auto_now_add=True , null=True , blank=True)

    @property
    def want_to_read_images(self):
        return self.want_to_read_users.all()[0:3]

    @property
    def currently_reading_images(self):
        return self.currently_users.all()[0:3]
    
    @property
    def avg_rating(self):
        return self.review_set.only('rating').aggregate(Avg('rating'))['rating__avg']
    
    @property
    def total_reviews(self):
        return self.review_set.count()

    @property
    def total_want_to_read(self):
        return self.want_to_read_users.count()
    
    @property
    def total_reading(self):
        return self.currently_users.count()
    

    def __str__(self) -> str:
        return f'{self.name} - {self.author.name}'








class UserComment(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    review = models.ForeignKey('Review' , on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.user.username}: {self.text}'




class Review(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser,blank=True, related_name='liked_reviews')
    comments = models.ManyToManyField(CustomUser , through='UserComment' , related_name='comments_reviews')
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.text[:50]}...'

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()


class Message(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, db_index=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} : {self.text[:50]}...'




class Post(models.Model):
    author = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    cover = models.ImageField(upload_to='posts/',default='defaults/post.jpg',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.title



class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(name='test')



class Product(models.Model):
    name = models.CharField(max_length=100)

    my_manager = ProductManager()
    objects = models.Manager()

    def __str__(self) -> str:
        return self.name

