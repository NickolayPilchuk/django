from django.urls import path
from .import views
from .views import BlogView


urlpatterns = [path('login',views.login1,name = 'login'),
               path('register',views.register,name = 'register'),
               path('',views.homepage,name = 'homepage'),
               path('blogs/<int:pk>',BlogView.as_view(),name = 'blog-detail'),
               path('news/<int:id>',views.news),
               path('profile',views.profile,name = 'profile'),
               path('profile/edit',views.edit),
               path('create',views.create,name='create_blog'),
               path('logout',views.logout_,name='logout'),
               path('blogs/<int:id>/add_news',views.adding_news),
               path('change_blogs',views.change,name = 'change'),
               path('delete/<int:blog_pk>',views.delete,name = 'delete'),
               path('change/<int:blog_pk>',views.change_name,name = 'change_name'),
               path('change_img/<int:blog_pk>',views.change_image,name = 'change_img')]