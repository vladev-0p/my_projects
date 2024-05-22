"""
URL configuration for starsinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path

"""
from django.contrib import admin
from django.urls import path
from stars.views import index, categories, create_new_category, about, post, add_post, contact, login

urlpatterns = [
    path('create_new_category/', create_new_category),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('categories/<int:cat_id>/', categories),
    path('categories/<int:cat_id>/<str:name>/', categories),

    path('add_post/', add_post, name='add_post'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<int:post_id>/', post)
]

# #Обработка для несуществ страницы
# handler404 = error_page
