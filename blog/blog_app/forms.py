from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import News,Blog,Comments,UserExtended
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from captcha.fields import CaptchaField


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class ExtendedRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=20, label='Логин')
    firstname = forms.CharField(max_length=20,label='Имя')
    surname = forms.CharField(max_length=20,label='Фамилия')
    description = forms.CharField(required=False, max_length=20, label='О себе',widget=forms.Textarea)
    password1 = forms.CharField(required=True, max_length=20, label='Пароль')
    password2 = forms.CharField(required=True, max_length=20, label='Подтверждение пароля')
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('username','firstname','surname','password1','password2')

class EditForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    description = forms.CharField(max_length=500,widget=forms.Textarea())

class Blog_form(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Blog
        fields = ['name','images']

class Comment_form(forms.ModelForm):
    text = forms.CharField(max_length=20000, widget=forms.Textarea(attrs={'rows':4}))
    captcha = CaptchaField()
    class Meta:
        model = Comments
        fields = ['text','images']

class News_form(forms.ModelForm):
    text = forms.CharField(max_length=20000, widget=CKEditorUploadingWidget())
    captcha = CaptchaField()
    class Meta:
        model = News
        fields = ['title', 'text', 'images']

class Userpic_form(forms.ModelForm):
    userpic = forms.ImageField(label='')
    class Meta:
        model = UserExtended
        fields = ['userpic']

class name_form(forms.Form):
    name = forms.CharField(max_length=20,label='Введите новое имя')

class image_form(forms.Form):
    image = forms.ImageField(label='')