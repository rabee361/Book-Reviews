import django_filters
from .models import Book , Genre


#----this method needs the exact genre name----#
class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name="author__name", lookup_expr='icontains')
    genres = django_filters.ModelMultipleChoiceFilter(field_name="genre__name", to_field_name='name', queryset=Genre.objects.all())

    class Meta: 
        model = Book
        fields = ['author', 'genres']



class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name="author__username", lookup_expr='icontains')
    genres = django_filters.ModelMultipleChoiceFilter(field_name="genre__name", to_field_name='name', queryset=Genre.objects.all())

    class Meta: 
        model = Book
        fields = ['author', 'genres']