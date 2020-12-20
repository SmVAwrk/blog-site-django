from datetime import datetime

from django.test import TestCase

from blog_app.models import *


class BaseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.category = Categories.objects.create(title='Test category', slug='test-category')
        cls.tag_1 = Tags.objects.create(title='Test tag 1', slug='test-tag-1')
        cls.tag_2 = Tags.objects.create(title='Test tag 2', slug='test-tag-2')
        cls.post = Posts.objects.create(
            title='Test post',
            slug='test-post',
            author=cls.user,
            content='Test content',
            category=cls.category,
        )
        cls.post.tags.add(cls.tag_1, cls.tag_2)
        cls.comment = Comments.objects.create(
            post=cls.post,
            content='Test comment content 1, test comment content 2 and (not_visible)',
            author=cls.user,
        )


class CategoriesModelTest(BaseModelTest):

    def test_title(self):
        field_label = self.category._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название')

        max_length = self.category._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_slug(self):
        field_label = self.category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'URL')

        max_length = self.category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

        is_unique = self.category._meta.get_field('slug').unique
        self.assertTrue(is_unique)

    def test_object_name_is_title(self):
        object_name = self.category
        expected_object_name = self.category.title
        self.assertEquals(str(object_name), expected_object_name)

    def test_get_absolute_url(self):
        get_absolute_url = self.category.get_absolute_url()
        self.assertEquals(get_absolute_url, '/category/test-category/')


class TagsModelTest(BaseModelTest):

    def test_title(self):
        field_label = self.tag_1._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название')

        max_length = self.tag_1._meta.get_field('title').max_length
        self.assertEquals(max_length, 50)

    def test_slug(self):
        field_label = self.tag_1._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'URL')

        max_length = self.tag_1._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

        is_unique = self.tag_1._meta.get_field('slug').unique
        self.assertTrue(is_unique)

    def test_object_name_is_title(self):
        object_name = self.tag_1
        expected_object_name = self.tag_1.title
        self.assertEquals(str(object_name), expected_object_name)

    def test_get_absolute_url(self):
        get_absolute_url = self.tag_1.get_absolute_url()
        self.assertEquals(get_absolute_url, '/tag/test-tag-1/')


class PostsModelTest(BaseModelTest):

    def test_title(self):
        field_label = self.post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название')

        max_length = self.post._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_slug(self):
        field_label = self.post._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'URL')

        max_length = self.post._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

        is_unique = self.post._meta.get_field('slug').unique
        self.assertTrue(is_unique)

    def test_author(self):
        field_label = self.post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_content(self):
        field_label = self.post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Контент поста')

        is_blank = self.post._meta.get_field('content').blank
        self.assertTrue(is_blank)

    def test_created_at(self):
        field_label = self.post._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

        is_auto_now_add = self.post._meta.get_field('created_at').auto_now_add
        self.assertTrue(is_auto_now_add)

    def test_updated_at(self):
        field_label = self.post._meta.get_field('updated_at').verbose_name
        self.assertEquals(field_label, 'Дата обновления')

        is_auto_now = self.post._meta.get_field('updated_at').auto_now
        self.assertTrue(is_auto_now)

    def test_photo(self):
        field_label = self.post._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'Фото')

        is_blank = self.post._meta.get_field('photo').blank
        self.assertTrue(is_blank)

        upload_path = self.post._meta.get_field('photo').upload_to
        self.assertEquals(upload_path, 'photos/%Y/%m/%d/')

    def test_views(self):
        field_label = self.post._meta.get_field('views').verbose_name
        self.assertEquals(field_label, 'Кол-во просмотров')

        default = self.post._meta.get_field('views').default
        self.assertEquals(default, 0)

    def test_category(self):
        field_label = self.post._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'Категория')


    def test_tags(self):
        field_label = self.post._meta.get_field('tags').verbose_name
        self.assertEquals(field_label, 'Теги')


        is_blank = self.post._meta.get_field('tags').blank
        self.assertTrue(is_blank)

    def test_is_published(self):
        field_label = self.post._meta.get_field('is_published').verbose_name
        self.assertEquals(field_label, 'Публикация')

        default = self.post._meta.get_field('is_published').default
        self.assertFalse(default)

    def test_on_main(self):
        field_label = self.post._meta.get_field('on_main').verbose_name
        self.assertEquals(field_label, 'Закрепленно')

        default = self.post._meta.get_field('on_main').default
        self.assertFalse(default)

    def test_object_name_is_title(self):
        object_name = self.post
        expected_object_name = self.post.title
        self.assertEquals(str(object_name), expected_object_name)

    def test_get_absolute_url(self):
        get_absolute_url = self.post.get_absolute_url()
        self.assertEquals(get_absolute_url, '/post/test-post/')


class CommentsModelTest(BaseModelTest):

    def test_post(self):
        field_label = self.comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Пост')

    def test_content(self):
        field_label = self.post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Контент поста')

        is_blank = self.post._meta.get_field('content').blank
        self.assertTrue(is_blank)

    def test_author(self):
        field_label = self.post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_created_at(self):
        field_label = self.post._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

        is_auto_now_add = self.post._meta.get_field('created_at').auto_now_add
        self.assertTrue(is_auto_now_add)

    def test_object_name_is_content_50(self):
        object_name = self.comment
        expected_object_name = 'Test comment content 1, test comment content 2 and'
        self.assertEquals(str(object_name), expected_object_name)