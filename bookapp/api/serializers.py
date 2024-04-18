from rest_framework import serializers
from bookapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password





class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','first_name','last_name','image','total_reviews','want_to_read','currently_reading','read']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name','image','about','followers','total_followers']



class QuoteSerialzier(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name',read_only=True)
    image = serializers.ImageField(source='author.image',read_only=True)

    class Meta:
        model = Quote
        fields = ['text','author','author_name','image']

    


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    quotes = QuoteSerialzier(many=True,read_only=True)
    genre = GenreSerializer(many=True , read_only=True)
    want_to_read_images = serializers.SerializerMethodField()
    currently_reading_images = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields  = ['id','name','author','avg_rating','total_reviews','cover','about','quotes','genre','pages','total_want_to_read','total_reading','want_to_read_images','currently_reading_images']
   
    
    def get_want_to_read_images(self,obj):
        request = self.context.get('request')
        arr = []
        for i in obj.want_to_read_images:
            x = request.build_absolute_uri(i.image.url)
            arr.append(x)
        return arr

    def get_currently_reading_images(self,obj):
        request = self.context.get('request')
        arr = []
        for i in obj.currently_reading_images:
            x = request.build_absolute_uri(i.image.url)
            arr.append(x)
        return arr




class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username','image','email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("passwords don't match")
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        login(request,user)
        return user





class MessageSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=False,read_only=True)
    class Meta:
        model = Message
        fields = ['user','text']

    def create(self, validated_data):
        request = self.context.get('request')
        msg = Message.objects.create(user=request.user,text=validated_data['text'])
        msg.save()
        return msg



class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(CustomUser,many=False,read_only=True)
    book_name = serializers.CharField(source = 'book.name' ,read_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['user','book_name','text','rating','created','likes','total_likes','total_comments']

    def get_created(self,obj):
        return obj.created.strftime('%Y-%m-%d')



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'