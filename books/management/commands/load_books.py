import csv
from django.core.management.base import BaseCommand
from books.models import Book, Author
from django.db import transaction

class Command(BaseCommand):
    help = 'Import books from books.csv using bulk_create for performance'

    def handle(self, *args, **options):
        try:
            with open('books.csv', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                print("CSV Headers:", reader.fieldnames)

                # Clear old data (for dev/testing only)
                Book.objects.all().delete()

                authors_cache = {}
                books_batch = []
                batch_size = 100
                count = 0
                fake_id = 1000

                for row in reader:
                    # Cache authors to avoid duplicate DB hits
                    author_name = row['author'].strip()
                    if author_name in authors_cache:
                        author = authors_cache[author_name]
                    else:
                        author, _ = Author.objects.get_or_create(name=author_name)
                        authors_cache[author_name] = author

                    books_batch.append(Book(
                        gutenberg_id=fake_id,
                        title=row['title'].strip(),
                        language=row['language'].strip(),
                        downloads=int(row['downloads']),
                        author=author
                    ))
                    fake_id += 1
                    count += 1

                    # Bulk insert in chunks
                    if len(books_batch) >= batch_size:
                        Book.objects.bulk_create(books_batch)
                        books_batch.clear()

                # Final batch
                if books_batch:
                    Book.objects.bulk_create(books_batch)

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} books using bulk_create.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
