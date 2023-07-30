from django.shortcuts import render,redirect,HttpResponse
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import UserExtended,Blog,News,Comments
from django.views import generic
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, timedelta


def login1(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request=request,user=user)
                return redirect(homepage)
            else:
                messages.error(request,'Юзер неверный')
                return redirect(login1)
    else:
        form = AuthForm()
    return render(request,'blog_app/login.html',{'form':form,'title':'Войти'})

def register(request):
    if request.method == 'POST':
        form = ExtendedRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            firstname = form.cleaned_data.get('firstname')
            surname = form.cleaned_data.get('surname')
            description = form.cleaned_data.get('description')
            password = form.cleaned_data.get('password1')
            UserExtended.objects.create(user=user,
                                        firstname=firstname,
                                        surname=surname,
                                        description=description)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Вы успешно зарегистрировались')
                return redirect(homepage)
    else:
        form = ExtendedRegisterForm()
    return render(request,'blog_app/registration.html',{'form':form,'user': request.user,'title':'Зарегистрироваться'})

class BlogView(generic.DetailView):
    model = Blog
    template_name = 'blog_details.html'
    context_object_name = 'blog'
    queryset = Blog.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all().filter(blog=self.get_object()).order_by('-ctime')
        p = Paginator(news, 5)
        page_number = self.request.GET.get('page')
        page_obj = p.get_page(page_number)
        context['page_obj']=page_obj
        return context

def news(request,id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = Comment_form(request.POST,request.FILES)
            comment = form.save(commit=False)
            comment.news = News.objects.get(id=id)
            comment.user = request.user
            comment.save()
            return redirect(news,id)
        else:
            return redirect(login1)
    else:
        this_news = News.objects.get(pk = id)
        blog = Blog.objects.get(news = this_news)
        comments = Comments.objects.filter(news = this_news).order_by('-ctime')
        p = Paginator(comments, 5)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        form = Comment_form()
        return render(request,'news_details.html',{'comments':comments,'news':this_news,'blog':blog,'form':form,'page_obj':page_obj})

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Userpic_form(request.POST,request.FILES)
            if form.is_valid():
                user = UserExtended.objects.get(user=request.user)
                user.userpic = request.FILES['userpic']
                user.save()
                messages.success(request, 'Аватарка изменена')
                return redirect(profile)
            else:                           #Сообщения прихуячить
                return HttpResponse("ХУЙ")
        else:
            form = Userpic_form()
            user = request.user
            return render(request,'blog_app/profile.html',{'user':user,'form':form})

def homepage(request):
    blogs = Blog.objects.all().order_by('-ctime')
    p = Paginator(blogs,5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'blogs':blogs,'request':request,'page_obj':page_obj}
    return render(request,'blog_app/homepage.html',context)

def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES)
        if form.is_valid():
            user = UserExtended.objects.get(user=request.user)
            user.description = form.cleaned_data.get('description')
            user.firstname = form.cleaned_data.get('firstname')
            user.surname = form.cleaned_data.get('surname')
            user.save()
            messages.success(request, 'Данные изменены')
            return redirect(homepage)
    else:
        user =UserExtended.objects.get(user=request.user)
        form = EditForm(initial={'description':user.description,'firstname': user.firstname,'surname':user.surname})
    return render(request,'blog_app/edit.html',{'form':form})


def create(request):        #Создание блога
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Blog_form(request.POST,request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.user = request.user
                blog.save()
                messages.success(request, 'Блог создан')
                return redirect(homepage)
        else:
            form = Blog_form()
        return render(request,'blog_app/create_blog.html',{'form':form})
    else:
        return redirect(login1)

def logout_(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли')
    return redirect(homepage)


def adding_news(request,id):
    blog = Blog.objects.get(id=id)
    if request.user == blog.user:
        if request.method == 'POST':
            form = News_form(request.POST,request.FILES)
            if request.user==blog.user:
                if form.is_valid():
                    news = form.save(commit=False)
                    news.blog = blog
                    news.save()
                    messages.success(request, 'Новость создана')
                    blog.ctime = datetime.now()
                    blog.save()
                    return redirect('blog-detail',id)
        else:
            form = News_form()
        return render(request, 'blog_app/add_news.html', {'form': form})
    else:
        messages.error(request,'Вы не создатель блога')
        return redirect(homepage)

def change(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    return render(request,'blog_app/change_blogs.html',{'blogs':blogs})

def delete(request,blog_pk):
    if request.user == blog.user:
        Blog.objects.get(pk=blog_pk).delete()
        messages.info(request,'Блог удален')
        return redirect(change)
    else:
        messages.error(request,'Ошибка доступа')
        return redirect(homepage)

def change_name(request,blog_pk):
    blog = Blog.objects.get(pk=blog_pk)
    if request.user == blog.user:
        if request.method == 'POST':
            form = name_form(request.POST)
            if form.is_valid():
                blog.name=form.cleaned_data.get('name')
                blog.save()
                messages.info(request,'Название изменено')
                return redirect(change)
        else:
            form = name_form
        return render(request,'blog_app/create_blog.html',{'form':form,'title':'Изменение названия'})
    else:
        messages.error(request,'Ошибка доступа')
        return redirect(homepage)

def change_image(request,blog_pk):
    blog = Blog.objects.get(pk=blog_pk)
    if request.user == blog.user:
        if request.method == 'POST':
            blog.images=request.FILES['image']
            blog.save()
            messages.info(request,'Картинка изменена')
            return redirect(change)
        else:
            form = image_form
        return render(request,'blog_app/create_blog.html',{'form':form,'title':'Изменение картинки'})
    else:
        messages.error(request,'Ошибка доступа')
        return redirect(homepage)

