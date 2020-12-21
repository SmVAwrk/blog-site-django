import re

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from blog_app.models import Posts, Comments


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователей на сайте в модель User"""
    username = forms.CharField(label='Имя пользователя', help_text='Не более 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    """Форма для входа пользователей"""
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddPostForm(forms.ModelForm):
    """
    Форма, связанная с моделью, для добавления поста на сайт.
    Через виджеты к полю контент подключен CKEditor
    """
    class Meta:
        model = Posts
        fields = ['title', 'content', 'photo', 'category', 'is_published']
        attrs = {'class': 'form-control'}
        widgets = {
            'title': forms.TextInput(attrs=attrs),
            'content': CKEditorUploadingWidget(),
            'photo': forms.FileInput(attrs=attrs),
            'category': forms.Select(attrs=attrs),
        }

    def clean_title(self):
        """Кастомный валидатор для проверки названия новости"""
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры.')
        return title


class AddCommentForm(forms.ModelForm):
    """Форма для добавления комментария к посту"""
    class Meta:
        model = Comments
        fields = ['content', ]
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})}


