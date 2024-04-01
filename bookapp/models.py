from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg , Count
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property



class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    


class CustomUser(AbstractUser):
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='users', default='default/account.png')

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

    def __str__(self) -> str:
        return f'{self.text[:50]}...'



class Book(models.Model):
    LANGUAGES = (
        ('en' , 'English'),
        ('ar' , 'Arabic')
    )
    name = models.CharField(max_length=150 , db_index=True , default="none")
    cover = models.ImageField(upload_to='covres/')
    about = models.TextField(default='none')
    author = models.ManyToManyField(Author)
    pages = models.IntegerField(default=250)
    language = models.CharField(max_length=30,choices=LANGUAGES , default='en')
    genre = models.ManyToManyField(Genre)
    quotes = models.ManyToManyField(Quote ,blank=True)

    @property
    def avg_rating(self):
        return self.review_set.only('rating').aggregate(Avg('rating'))['rating__avg']
    
    @property
    def total_reviews(self):
        return self.review_set.count()

    def __str__(self) -> str:
        author_names = ", ".join([str(author) for author in self.author.all()])
        return f'{self.name} - {author_names}'




class ReadingList(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def __str__(self) -> str:
        return self.user.username




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
    date = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.title




class Product(models.Model):
    name = models.CharField(max_length=100)

    def delete(self,*args,**kwargs):
        print(f"Deleting {self.name}")
        super().delete(*args, **kwargs)
        print(f"{self.name} has been deleted")


    def __str__(self) -> str:
        return self.name

