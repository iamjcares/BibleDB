from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Book, Chapter, Verse, VerseVersion, Version
from .serializers import (BookSerializer, ChapterSerializer,
                          VerseVersionSerializer, VersionSerializer)


class VersesByBookVersionView(generics.ListAPIView):
    serializer_class = VerseVersionSerializer

    def get_queryset(self):
        book_name = self.kwargs['book']
        version_slug = self.kwargs['version']
        return VerseVersion.objects.filter(
            verse__chapter__book__name=book_name,
            version__slug=version_slug
        )

class VersionListView(generics.ListAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ChapterListView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Chapter.objects.filter(book__id=book_id)
    
class ChapterByNameListView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_name = self.kwargs['book_name']
        return Chapter.objects.filter(book__name=book_name)

class VersesByChapterView(generics.ListAPIView):
    serializer_class = VerseVersionSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        version_id = self.kwargs['version_id']
        return VerseVersion.objects.filter(
            verse__chapter__id=chapter_id,
            version__id=version_id
        )
        
class VersesByChapterNumberView(generics.ListAPIView):
    serializer_class = VerseVersionSerializer

    def get_queryset(self):
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name']
        return VerseVersion.objects.filter(
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

class SingleVerseByNumberView(generics.RetrieveAPIView):
    serializer_class = VerseVersionSerializer
    lookup_field = 'verse__verse'

    def get_queryset(self):
        book_name = self.kwargs['book_name']
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name']
        return VerseVersion.objects.filter(
            verse__chapter__book__name=book_name,
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

class VerseWithPreviousAndNextView(generics.RetrieveAPIView):
    serializer_class = VerseVersionSerializer
    lookup_field = 'verse__verse'

    def get_queryset(self):
        book_name = self.kwargs['book_name']
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name']
        return VerseVersion.objects.filter(
            verse__chapter__book__name=book_name,
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

    def get(self, request, *args, **kwargs):
        current_verse = self.get_object()
        previous_verse = VerseVersion.objects.filter(
            verse__chapter__book__name=self.kwargs['book_name'],
            verse__chapter__chapter_number=self.kwargs['chapter_number'],
            version__name=self.kwargs['version_name'],
            verse__verse_number=current_verse.verse.verse_number - 1
        ).first()

        next_verse = VerseVersion.objects.filter(
            verse__chapter__book__name=self.kwargs['book_name'],
            verse__chapter__chapter_number=self.kwargs['chapter_number'],
            version__name=self.kwargs['version_name'],
            verse__verse_number=current_verse.verse.verse_number + 1
        ).first()

        serializer = self.get_serializer([current_verse, previous_verse, next_verse], many=True)
        return Response(serializer.data)