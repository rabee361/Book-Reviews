from django.urls import path , include
from .views import *


urlpatterns = [
    path('log-in/' , Login.as_view(), name="login"),
    path('sign-up/' , SignUp.as_view() , name='sign-up'),
    path('logout/' , Logout.as_view() , name="logout"),
    path('books/' , AllBooks.as_view() , name="books"),
    path('books/<str:pk>/' , GetBook.as_view() , name="single_book"),
    path('featured/' ,LatestBooks.as_view() , name="latest"),
    path('lartest/' , FeaturedBooks.as_view() , name="featured"),
    path('select-genres/' , SelectGenres.as_view() , name="select-genres"),
    path('want-to-read/<str:pk>/' , WantToRead.as_view() , name="want-to-read"),
    path('currently-reading/<str:pk>/' , CurrentlyReading.as_view() , name="currently-reading"),
    path('read-book/<str:pk>/' , Read.as_view() , name="read-book"),
    path('genres1/' , GetGenres.as_view() , name="genres"),
    path('quotes/' , ListQuote.as_view() , name="list-quotes"),
    path('authors/' , ListAuthors.as_view() , name="authors"),
    path('author/<str:pk>' , GetAuthor.as_view() , name="get-author"),
    path('related-books/<str:pk>/' , RelatedBooks.as_view() , name="related_books"),
    path('message/' , WriteMessage.as_view() , name="message"),
    path('reviews/<str:pk>/' , BookReviews.as_view() , name="reviews"),
    path('posts/' , ListPosts.as_view() , name="list-posts"),
    path('get-post/<str:pk>' , GetPost.as_view() , name="get-post"),
]