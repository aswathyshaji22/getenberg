from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer
from django.core.management import call_command

class BookListView(APIView):
    """
    API endpoint to retrieve books with filters, pagination, and sorting.
    Supports filtering by ID, language, mime-type, topic, author, and title.
    Returns a paginated JSON response with 25 books per page sorted by downloads.
    """

    def get(self, request):
        books = Book.objects.all()

        # --- Get query parameters ---
        id_param = request.GET.get('id')
        language_param = request.GET.get('language')
        mime_type_param = request.GET.get('mime-type')
        topic_param = request.GET.get('topic')
        author_param = request.GET.get('author')
        title_param = request.GET.get('title')

        # --- Filter by Gutenberg IDs ---
        if id_param:
            id_list = [int(i.strip()) for i in id_param.split(',') if i.strip().isdigit()]
            books = books.filter(gutenberg_id__in=id_list)

        # --- Filter by language code ---
        if language_param:
            languages = [lang.strip() for lang in language_param.split(',')]
            books = books.filter(language__in=languages)

        # --- Filter by MIME type ---
        if mime_type_param:
            mime_types = [mt.strip() for mt in mime_type_param.split(',')]
            books = books.filter(formats__mime_type__in=mime_types)

        # --- Filter by topic (subject or bookshelf) ---
        if topic_param:
            topics = [t.strip() for t in topic_param.split(',')]
            topic_query = Q()
            for topic in topics:
                topic_query |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
            books = books.filter(topic_query)

        # --- Filter by author name (partial match) ---
        if author_param:
            for author in author_param.split(','):
                books = books.filter(author__name__icontains=author.strip())

        # --- Filter by title (partial match) ---
        if title_param:
            for title in title_param.split(','):
                books = books.filter(title__icontains=title.strip())

        # --- Sort by popularity ---
        books = books.order_by('-downloads').distinct()

        # --- Pagination (25 per page) ---
        try:
            page = max(1, int(request.GET.get('page', 1)))
        except ValueError:
            page = 1
        page_size = 25
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        total_books = books.count()

        # --- Serialize the response ---
        serialized_books = BookSerializer(books[start_index:end_index], many=True)

        return Response({
            'total': total_books,
            'page': page,
            'books': serialized_books.data
        }, status=status.HTTP_200_OK)



class RunMigrationsView(APIView):
    """
    Temporary API endpoint to run Django migrations.
    Only for admin use. DELETE this after running once!
    """

    def post(self, request):
        try:
            call_command('migrate')
            return Response({"message": "✅ Migrations ran successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
