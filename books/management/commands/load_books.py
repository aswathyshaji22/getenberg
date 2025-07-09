import csv
from django.core.management.base import BaseCommand
from books.models import Book, Author

class Command(BaseCommand):
    help = 'Load books from books.csv into the database'

    def handle(self, *args, **kwargs):
        with open('books/data/books.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                author, _ = Author.objects.get_or_create(name=row['author'])
                book, created = Book.objects.get_or_create(
                    title=row['title'],
                    author=author,
                    language=row.get('language', 'en'),
                    downloads=int(row.get('downloads', 0)),
                    gutenberg_id=100000 + count
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {count} books"))
