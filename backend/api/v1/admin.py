from django.contrib import admin

from .models import *


class ManuscriptAdmin(admin.ModelAdmin):
    # какие поля модели мы будем видеть в списке
    # list_display = ('title', 'author', 'storage', 'creation_date')
    # по каким полям мы можем искать
    # search_fields = ('title', 'author', 'storage', 'creation_date')
    # что мы можем модифицировать из списка (не открывая запись)
    list_editable = ()
    # по каким параметрам можно фильтровать
    # list_filter = ('id', 'manuscript', )


class ImageAdmin(admin.ModelAdmin):
    # какие поля модели мы будем видеть в списке
    list_display = ('id', 'image', 'manuscript', 'folio_number', 'part_of_folio')
    # по каким полям мы можем искать
    # search_fields = ('id', 'manuscript')
    # что мы можем модифицировать из списка (не открывая запись)
    list_editable = ()
    # по каким параметрам можно фильтровать
    list_filter = ('manuscript',)


# Register your models here.
admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(Image, ImageAdmin)
