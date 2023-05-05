from django.urls import path

from . import views

urlpatterns = [
    
    path('versions/', views.VersionListView.as_view(), name='versions'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:book_id>/chapters/', views.ChapterListView.as_view(), name='chapters'),
    path('books/<str:book_name>/chapters/', views.ChapterByNameListView.as_view(), name='chaptersbyname'),
    path('versions/<int:version_id>/chapters/<int:chapter_id>/verses/', views.VersesByChapterView.as_view(), name='verses_by_chapter'),
    path('versions/<str:version_name>/books/<str:book_name>/chapters/<int:chapter_number>/verses/', views.VersesByChapterNumberView.as_view(), name='verses_by_chapter_number'),

    path('versions/<str:version_name>/books/<str:book_name>/chapters/<int:chapter_number>/verses/<int:verse>/', views.SingleVerseByNumberView.as_view(), name='single_verse_by_number'),
    # path('versions/<str:version_name>/books/<str:book_name>/chapters/<int:chapter_number>/verses/<int:verse>/with-prev-next/', views.VerseWithPreviousAndNextView.as_view(), name='verse_with_prev_next'),
]
