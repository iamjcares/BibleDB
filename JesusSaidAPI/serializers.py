from rest_framework import serializers

from .models import Book, Chapter, Verse, VerseVersion, Version


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id', 'name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter']

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id','chapter', 'verse', 'by_jesus', 'qotd']
        
class VerseVersionSerializer(serializers.ModelSerializer):
    # book = serializers.CharField(source='verse.chapter.book.name')
    # chapter = serializers.IntegerField(source='verse.chapter.chapter')
    # version = serializers.CharField(source='version.name')
    verse = serializers.IntegerField(source='verse.verse')
    spoken_by_jesus = serializers.BooleanField(source='verse.by_jesus')
    qotd = serializers.CharField(source='verse.qotd')
    class Meta:
        model = VerseVersion
        fields = ['text', 'verse', 'spoken_by_jesus', 'qotd']


