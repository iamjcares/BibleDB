from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Book, Chapter, Verse, VerseVersion, Version
from .serializers import (BookSerializer, ChapterSerializer,
                          VerseVersionSerializer, VersionSerializer)


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
        book_name = self.kwargs['book_name'].lower()
        return Chapter.objects.filter(book__name=book_name)


class VersesByChapterView(generics.ListAPIView):
    serializer_class = VerseVersionSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        version_id = self.kwargs['version_id']
        return VerseVersion.objects.select_related('verse').filter(
            verse__chapter__id=chapter_id,
            version__id=version_id
        )
        
class VersesByChapterNumberView(generics.ListAPIView):
    serializer_class = VerseVersionSerializer

    def get_queryset(self):
        book_name = self.kwargs['book_name'].lower()
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name'].lower()
        return VerseVersion.objects.select_related('verse').filter(
            verse__chapter__book__name=book_name,
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

class SingleVerseByNumberView(generics.RetrieveAPIView):
    serializer_class = VerseVersionSerializer
    lookup_field = 'verse__verse'
    lookup_url_kwarg = 'verse'

    def get_queryset(self):
        book_name = self.kwargs['book_name'].lower()
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name'].lower()
        return VerseVersion.objects.filter(
            verse__chapter__book__name=book_name,
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

class VerseWithPreviousAndNextView(generics.RetrieveAPIView):
    serializer_class = VerseVersionSerializer
    lookup_field = 'verse__verse'
    lookup_url_kwarg = 'verse'

    def get_queryset(self):
        book_name = self.kwargs['book_name'].lower()
        chapter_number = self.kwargs['chapter_number']
        version_name = self.kwargs['version_name'].lower()
        return VerseVersion.objects.filter(
            verse__chapter__book__name=book_name,
            verse__chapter__chapter=chapter_number,
            version__slug=version_name
        )

    def get(self, request, *args, **kwargs):
        current_verse = self.get_object()
        previous_verse = VerseVersion.objects.filter(
            verse__chapter__book__name=self.kwargs['book_name'].lower(),
            verse__chapter__chapter=self.kwargs['chapter_number'],
            version__slug=self.kwargs['version_name'].lower(),
            verse__verse=current_verse.verse.verse - 1
        ).first()

        next_verse = VerseVersion.objects.filter(
            verse__chapter__book__name=self.kwargs['book_name'].lower(),
            verse__chapter__chapter=self.kwargs['chapter_number'],
            version__slug=self.kwargs['version_name'].lower(),
            verse__verse=current_verse.verse.verse + 1
        ).first()
        
        print(current_verse, next_verse)
        

        serializer = self.get_serializer([previous_verse, current_verse, next_verse], many=True)
        return Response(serializer.data)