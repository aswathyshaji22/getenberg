from django.db import models

class Author(models.Model):
    """
    Represents an author of one or more books.
    """
    name = models.CharField(max_length=128)
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    Represents a subject or theme that can be assigned to books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bookshelf(models.Model):
    """
    Represents a bookshelf category (e.g., 'Science Fiction', 'Children's Literature').
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Format(models.Model):
    """
    Represents a downloadable format of a book (e.g., EPUB, plain text).
    """
    mime_type = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.mime_type}"


class Book(models.Model):
    """
    Represents a book and its metadata including author, subjects, formats, and download stats.
    """
    title = models.CharField(max_length=255)
    gutenberg_id = models.IntegerField(unique=True)
    language = models.CharField(max_length=10)
    downloads = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    bookshelves = models.ManyToManyField(Bookshelf)
    formats = models.ManyToManyField(Format)

    def __str__(self):
        return self.title