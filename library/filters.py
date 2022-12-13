from .models import LibraryBook, BookDistribution
import django_filters


class BookFilter(django_filters.FilterSet):
    
    class Meta:
        model = LibraryBook
        fields = ['name']
        
        
class BookDistributionFilter(django_filters.FilterSet):
    class Meta:
        model = BookDistribution
        fields = ['book_number']
