from django.urls import path

from . import views

urlpatterns = [
    path('verses/<str:book_name>/<str:version_name>/', views.VersesByBookVersionView.as_view(), name='verses_by_book_version'),
    path('versions/', views.VersionListView.as_view(), name='versions'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:book_id>/chapters/', views.ChapterListView.as_view(), name='chapters'),
    path('books/<str:book_name>/chapters/', views.ChapterByNameListView.as_view(), name='chaptersbyname'),
    path('chapters/<int:chapter_id>/verses/<int:version_id>/', views.VersesByChapterView.as_view(), name='verses_by_chapter'),
    path('chapters/<str:chapter_number>/verses/<str:version_name>/', views.VersesByChapterNumberView.as_view(), name='verses_by_chapter_number'),
    path('verses/<str:book_name>/<int:chapter_number>/<str:version_name>/<int:verse_number>/', views.SingleVerseByNumberView.as_view(), name='single_verse_by_number'),
    path('verses/<str:book_name>/<int:chapter_number>/<str:version_name>/<int:verse_number>/with-prev-next/', views.VerseWithPreviousAndNextView.as_view(), name='verse_with_prev_next'),
]
