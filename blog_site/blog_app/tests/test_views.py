from pprint import pprint

from django.contrib import messages
from django.test import TestCase, Client

from blog_app.forms import AddCommentForm
from blog_app.models import *


class BaseViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        cls.category = Categories.objects.create(title='Test category', slug='test-category')
        cls.tag_1 = Tags.objects.create(title='Test tag 1', slug='test-tag-1')
        number_of_posts = 5
        for num in range(number_of_posts):
            cls.post = Posts.objects.create(
                title=f'Test post {num}',
                slug=f'test-post-{num}',
                author=cls.user,
                content=f'Test content {num}',
                category=cls.category,
                is_published=True,
                on_main=False
            )
            cls.post.tags.add(cls.tag_1)

        cls.comment = Comments.objects.create(
            post=cls.post,
            content='Test comment content',
            author=cls.user
        )
        cls.search_field = 'Test'


class HomeListViewTest(BaseViewTest):

    def test_view_url(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('home'))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/index.html')

    def test_view_pagination(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['posts']), 4)

        response_sec_page = self.client.get(reverse('home') + '?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response_sec_page.context)
        self.assertTrue(response_sec_page.context['is_paginated'])
        self.assertEquals(len(response_sec_page.context['posts']), 1)

    def test_view_get_context_data(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Главная')


class PostsByCategoryListViewTest(BaseViewTest):

    def test_view_url(self):
        response = self.client.get(f'/category/{self.category.slug}/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/category.html')

    def test_view_pagination(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['posts']), 4)

        response_sec_page = self.client.get(reverse('category', kwargs={'slug': self.category.slug}) + '?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response_sec_page.context)
        self.assertTrue(response_sec_page.context['is_paginated'])
        self.assertEquals(len(response_sec_page.context['posts']), 1)

    def test_view_get_context_data(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Test category')


class PostsByTagListViewTest(BaseViewTest):

    def test_view_url(self):
        response = self.client.get(f'/tag/{self.tag_1.slug}/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('tag', kwargs={'slug': self.tag_1.slug}))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag_1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/category.html')

    def test_view_pagination(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag_1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['posts']), 4)

        response_sec_page = self.client.get(reverse('tag', kwargs={'slug': self.tag_1.slug}) + '?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response_sec_page.context)
        self.assertTrue(response_sec_page.context['is_paginated'])
        self.assertEquals(len(response_sec_page.context['posts']), 1)

    def test_view_get_context_data(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag_1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Тег: Test tag 1')


class GetPostDetailViewTest(BaseViewTest):

    def test_view_url(self):
        response = self.client.get(f'/post/{self.post.slug}/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/single.html')

    def test_view_get_context_data(self):
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.context['post_item'].views, 1)
        self.assertTrue(response.context['form'])
        self.assertTrue(self.comment in response.context['comments'])

    def test_view_post_method(self):
        self.client.login(username='test_user', password='test_password')
        response_1 = self.client.post(reverse('post', kwargs={'slug': self.post.slug}),
                                   {'form.content': 'Comment from test_user'})
        self.assertRedirects(response_1, reverse('post', kwargs={'slug': self.post.slug}))

        response_2 = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertEquals(response_2.status_code, 200)
        self.assertEquals(len(response_2.context['comments']), 2)


class SearchListViewTest(BaseViewTest):

    def test_view_url(self):
        response = self.client.get(f'/search/?s={self.search_field}')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('search') + f'?s={self.search_field}')
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('search') + f'?s={self.search_field}')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/search.html')

    def test_view_pagination(self):
        response = self.client.get(reverse('search') + f'?s={self.search_field}')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['posts']), 4)

        response_sec_page = self.client.get(reverse('search') + f'?s={self.search_field}' + '&page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response_sec_page.context)
        self.assertTrue(response_sec_page.context['is_paginated'])
        self.assertEquals(len(response_sec_page.context['posts']), 1)

    def test_view_get_context_data(self):
        response = self.client.get(reverse('search') + f'?s={self.search_field}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], f'Поиск по "{self.search_field}"')
        self.assertEquals(response.context['s'], f's={self.search_field}&')


class RegistrationFunctionView(BaseViewTest):

    def test_view_url(self):
        response = self.client.get('/registration/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('reg'))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('reg'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/registration.html')

    def test_view_get_context_data(self):
        response = self.client.get(reverse('reg'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Регистрация')
        self.assertTrue(response.context['form'])

    # def test_view_post_method(self):
    #     context_not_valid = {
    #         'form.username': 'test_user_2',
    #         'form.email': 'test_user@test.com',
    #         'form.password1': 'Pass1',
    #         'form.password2': 'Pass2',
    #     }
    #     response_not_valid = self.client.post(reverse('reg'), context_not_valid)
    #     self.assertEquals(response_not_valid.status_code, 200)
    #
    #     context_valid = {
    #         'form.username': 'test_user_2',
    #         'form.email': 'test_user@test.com',
    #         'form.password1': 'Exs4Lyyf7Ad3aeD',
    #         'form.password2': 'Exs4Lyyf7Ad3aeD',
    #     }
    #     response_valid = self.client.post(reverse('reg'), context_valid)
    #
    #     self.assertRedirects(response_valid, reverse('home'))


class LoginFunctionView(BaseViewTest):

    def test_view_url(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('login'))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/registration.html')

    def test_view_get_context_data(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Вход')
        self.assertTrue(response.context['form'])

    # def test_view_post_method(self):
        # context_not_valid = {
        #     'form.username': 'not_test_user',
        #     'form.password': 'test_password',
        # }
        # response_not_valid = self.client.post(reverse('reg'), context_not_valid)
        # self.assertEquals(response_not_valid.status_code, 200)

        # context_valid = {
        #     'form.username': 'test_user',
        #     'form.password': 'test_password',
        # }
        # response_valid = self.client.post(reverse('login'), context_valid)
        #
        # pprint(response_valid.method)
        # self.assertRedirects(response_valid, reverse('home'))


class AddPostFunctionViewTest(BaseViewTest):

    def test_view_url_no_login(self):
        response = self.client.get('/add_post/')
        self.assertRedirects(response, reverse('login'))

    def test_view_url_login(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get('/add_post/')
        self.assertEquals(response.status_code, 200)

        response_by_name = self.client.get(reverse('add_post'))
        self.assertEquals(response_by_name.status_code, 200)

    def test_view_template(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('add_post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/add_post.html')

    def test_view_get_context_data(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('add_post'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['title'], 'Добавление записи')
        self.assertTrue(response.context['form'])

    # def test_view_post_method(self):
        # self.client.login(username='test_user', password='test_password')
        #
        # context_valid = {
        #     'form.title': 'test_user',
        #     'form.content': 'test_password',
        #     'form.category': self.category,
        #     'form.is_published': True
        # }
        # response_valid = self.client.post(reverse('add_post'), context_valid)
        #
        # self.assertRedirects(response_valid, reverse('home'))

