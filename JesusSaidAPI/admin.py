from django.contrib import admin

from .models import Book, Chapter, Verse, VerseVersion, Version


# Register your models here.
class VerseVersionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'version', 'text_excerpt')
    search_fields = ('verse__chapter__book__name', 'verse__chapter__chapter', 'verse__verse', 'version__name', 'text')

    def text_excerpt(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_excerpt.short_description = 'Text Excerpt'


admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Verse)
admin.site.register(Version)
admin.site.register(VerseVersion, VerseVersionAdmin)
