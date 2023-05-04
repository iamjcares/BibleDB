from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)

class Version(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.IntegerField()

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    verse = models.IntegerField()
    by_jesus = models.BooleanField(default=False)
    qotd = models.IntegerField()

class VerseVersion(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    text = models.TextField()

class VerseAttribute(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    spoken_by_jesus = models.BooleanField()
    quote_of_the_day = models.BooleanField()
