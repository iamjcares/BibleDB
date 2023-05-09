from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name.title()

class Version(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    
    def __str__(self) -> str:
        return f'{self.name.title()} ({self.slug.upper()})' 

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.IntegerField()
    
    def __str__(self) -> str:
        return f'Chapter {self.chapter}'
        # return f'{self.book} Chapter {self.chapter}'

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    verse = models.IntegerField()
    by_jesus = models.BooleanField(default=False)
    qotd = models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return f'Verse {self.verse}'
        # return f'{self.chapter} Verse {self.verse}'

class VerseVersion(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.verse.chapter.book.name.title()} {self.verse.chapter.chapter}:{self.verse.verse} ({self.version.slug.upper()})'

class VerseAttribute(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    spoken_by_jesus = models.BooleanField()
    quote_of_the_day = models.BooleanField()
