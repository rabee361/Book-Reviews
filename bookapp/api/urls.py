from django.urls import path , include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductView)



urlpatterns = [
    path('log-in/' , Login.as_view(), name="login"),
    path('books/' , AllBooks.as_view() , name="books"),
    path('books/<str:pk>/' , GetBook.as_view() , name="single_book"),
    path('whoami/'  ,whoami.as_view() , name="whoami"),
    path('featured/' , FeaturedBooks.as_view() , name="featured"),
    path('select-genres/' , SelectGenres.as_view() , name="select-genres"),
    path('reading-list/' , GetReadingList.as_view() , name="reading-list"),
    path('genres/' , GetGenres.as_view() , name="genres"),
    path('authors/' , ListAuthors.as_view() , name="authors"),
    path('author/<str:pk>' , GetAuthor.as_view() , name="get-author"),
    path('related-books/<str:pk>/' , RelatedBooks.as_view() , name="related_books"),
    path('sign_up/', SignUp2.as_view() , name="sign_up"),
    path('login/' , Login.as_view() , name="login"),
    path('logout/' , Logout.as_view() , name="logout"),
    path('message/' , WriteMessage.as_view() , name="message"),
    path('reviews/<str:pk>/' , BookReviews.as_view() , name="reviews"),
    path('posts/' , ListPosts.as_view() , name="list-posts"),
    path('get-post/<str:pk>' , GetPost.as_view() , name="get-post"),
    path('test/' , Test.as_view()),
    path('', include(router.urls)),
]