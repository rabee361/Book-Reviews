from rest_framework.response import Response
from bookapp.models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView  ,ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from bookapp.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.contrib.auth import login , logout , authenticate
from django.shortcuts import redirect
from rest_framework import status
from django.contrib.auth.decorators import login_required
import stripe 
from django.conf import settings 
from rest_framework import viewsets
from django.db.models import F , Q , Sum , Window
from django.db.models.functions import Rank
import logging
from django.db import transaction


logger = logging.getLogger('django')
stripe.api_key = settings.STRIPE_SECRET_KEY

class CustomPagination(PageNumberPagination):
    page_size = 12




class whoami(APIView):
    def get(self,request):
        serializer = CustomUserSerializer(request.user,many=False)
        return Response(serializer.data)



class SignUp(APIView):
    def post(self,request):
        serializer = CustomUserSerializer(data=request.data , context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            



#-----login-----#
class Login(APIView):
    def get(self,request):
        return Response('hello , you can login here')
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            return Response("error")
        user = authenticate(username=username , password=password)
        if user:
            login(request,user)
            return Response("you're in !!!" , status=status.HTTP_200_OK)
            # return redirect('books')
        return Response('error' , status=status.HTTP_404_NOT_FOUND)


#----logout----#
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        logout(request)
        return Response('done')




class SelectGenres(APIView):
    def post(self,request):
        genres = request.data.get('genres')
        print(genres)
        user = request.user
        user.genres.add(*genres)
        print(user.genres)
        return Response("ok")



#-----get all books-----#
class AllBooks(ListAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter



class FeaturedBooks(APIView):
    def get(self,request):
        books = Book.objects.all().order_by('-id')
        serializer = BookSerializer(books,many=True,context={'request': request})
        return Response(serializer.data)



#-----get single book-----#
class GetBook(RetrieveAPIView):
    queryset = Book.objects.prefetch_related('author','genre','quotes').all()
    serializer_class = BookSerializer




#----get all genres----#
class GetGenres(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


#------get a single author-----#
class GetAuthor(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ListAuthors(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer 


#-----get other books from the same genre or writer-----#
class RelatedBooks(APIView):
    def get(self,request,pk):
        book = Book.objects.get(id=pk)
        genres = [i.name for i in book.genre.all()]
        books = Book.objects.prefetch_related('author','quotes','genre')\
                            .filter(Q(genre__name__in=genres))\
                            .distinct()[:8]
        serializer = BookSerializer(books,many=True,context={'request':request})
        return Response(serializer.data , status=status.HTTP_200_OK)
    


class ListQuote(ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerialzier



class WantToRead(APIView):
    def post(self,request,pk):
        book = Book.objects.get(id=pk)
        user = request.user
        user.want_to_read.add(book)
        serializer = CustomUserSerializer(user,many=False)
        return Response({
            "your want to read list":serializer.data['want_to_read']
        })





class CurrentlyReading(APIView):
    def post(self,request,pk):
        book = Book.objects.get(id=pk)
        user = request.user
        user.currently_reading.add(book)
        serializer = CustomUserSerializer(user,many=False)
        return Response({
            "your currently reading list":serializer.data['currently_reading']
        })


        
class Read(APIView):
    def post(self,request,pk):
        book = Book.objects.get(id=pk)
        user = request.user
        user.read.add(book)
        serializer = CustomUserSerializer(user,many=False)
        return Response({
            "your read books list":serializer.data['read']
        })


#-----sign up using apiview-----#
# class SignUp(APIView):
#     def post(self,request):
#         context = {'request':request}
#         serializer = UserSerializer(data=request.data , context=context)

#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#-----user writing a message/complaint----#
class WriteMessage(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]



class BookReviews(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Review.objects.filter(book=pk)
        serializer = self.get_serializer(queryset,many=True)
        return queryset




class ListPosts(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = PostFilter


class GetPost(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all
    serializer_class = PostSerializer



class Test(APIView):
    def get(self,request):
        query = Book.objects.get(id=1)
        serializer = BookSerializer(query,many=False)
        return Response(serializer.data)






class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class TestAPiView(APIView):
    def get(self,request):
        products = Product.my_manager.get(id=33)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)