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
        fields = ['chapter', 'verse', 'by_jesus', 'qotd']
        
class VerseVersionSerializer(serializers.ModelSerializer):
    verse = VerseSerializer(read_only=True)
    class Meta:
        model = VerseVersion
        fields = ['id', 'text', 'verse']