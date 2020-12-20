from django.test import TestCase

from blog_app.forms import AddPostForm, UserRegistrationForm, UserLoginForm
from blog_app.models import Categories


class UserRegistrationFormTest(TestCase):
    form = UserRegistrationForm()

    def test_username_field(self):
        field_label = self.form.fields['username'].label
        self.assertEquals(field_label, 'Имя пользователя')

        help_text = self.form.fields['username'].help_text
        self.assertEquals(help_text, 'Не более 150 символов')

    def test_email_field(self):
        field_label = self.form.fields['email'].label
        self.assertEquals(field_label, 'E-mail')

    def test_password1_field(self):
        field_label = self.form.fields['password1'].label
        self.assertEquals(field_label, 'Пароль')

    def test_password2_field(self):
        field_label = self.form.fields['password2'].label
        self.assertEquals(field_label, 'Повторите пароль')


class UserLoginFormTest(TestCase):
    form = UserLoginForm()

    def test_username_field(self):
        field_label = self.form.fields['username'].label
        self.assertEquals(field_label, 'Имя пользователя')

    def test_password_field(self):
        field_label = self.form.fields['password'].label
        self.assertEquals(field_label, 'Пароль')


class AddPostFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(title='Test category', slug='test-category')

    def test_custom_validation(self):
        form_data_valid = {
            'title': 'Test post',
            'content': 'Test content',
            'category': self.category
        }
        form_title_start_with_letter = AddPostForm(data=form_data_valid)
        self.assertTrue(form_title_start_with_letter.is_valid())

        form_data_not_valid = {
            'title': '1 Test post',
            'content': 'Test content',
            'category': self.category
        }
        form_title_start_with_digit = AddPostForm(data=form_data_not_valid)
        self.assertFalse(form_title_start_with_digit.is_valid())







