from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)


class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)


class PostsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Posts
        fields = '__all__'


class PostsAdmin(admin.ModelAdmin):
    form = PostsAdminForm
    save_as = True
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'updated_at', 'is_published', 'get_miniature')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'author',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'slug', 'author', 'category', 'content', 'photo', 'show_photo',
              'is_published', 'views', 'created_at', 'updated_at', 'tags',)
    readonly_fields = ('show_photo', 'views', 'created_at', 'updated_at',)

    def show_photo(self, obj):
        """Метод для просмотора добавленой фотографии во время редактирования в админке"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="300">')
        return '<->'
    show_photo.short_description = 'Просмотр фото'

    def get_miniature(self, obj):
        """Метод для просмотра миниатюры фотографии при просмотре списка постов в таблице"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '<Фото отсутствует>'
    get_miniature.short_description = 'Миниатюра'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Posts, PostsAdmin)



