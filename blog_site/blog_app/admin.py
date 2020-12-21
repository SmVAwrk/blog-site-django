from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CategoriesAdmin(admin.ModelAdmin):
    """Кастомизация модели Categories в админке"""
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)


class TagsAdmin(admin.ModelAdmin):
    """Кастомизация модели Tags в админке"""
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)


class PostsAdminForm(forms.ModelForm):
    """Форма для подключения CKEditor к полю content в моделе Posts"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Posts
        fields = '__all__'


class PostsAdmin(admin.ModelAdmin):
    """Кастомизация модели Posts в админке"""
    form = PostsAdminForm  # подключение CKEditor
    save_as = True
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'updated_at', 'is_published', 'get_miniature')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'author',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category', 'tags', 'on_main',)
    fields = ('title', 'slug', 'category', 'content', 'photo', 'show_photo',
              'is_published', 'views', 'created_at', 'updated_at', 'tags', 'on_main',)
    readonly_fields = ('show_photo', 'views', 'created_at', 'updated_at',)

    def show_photo(self, obj):
        """Метод для просмотора добавленой фотографии во время редактирования в админке"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="300">')
        return '-'
    show_photo.short_description = 'Просмотр фото'

    def get_miniature(self, obj):
        """Метод для просмотра миниатюры фотографии при просмотре списка постов в админке"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '<Фото отсутствует>'
    get_miniature.short_description = 'Миниатюра'

    def save_model(self, request, obj, form, change):
        """Добавление юзера как автора к создаваемому в админке посту"""
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class AdminComments(admin.ModelAdmin):
    """Кастомизация модели Comments в админке"""
    list_display = ('id', '__str__', 'post', 'author', 'created_at',)
    list_display_links = ('id', '__str__',)
    search_fields = ('__str__', 'author',)
    list_filter = ('post', 'author',)
    fields = ('content', 'post', 'author',)
    readonly_fields = ('post', 'author',)


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments, AdminComments)



