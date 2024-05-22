from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

from .models import Stars, Category

menu = [
    {'title': 'Главная', 'urlname': 'index'},
    {'title': 'О нас', 'urlname': 'about'},
    {'title': 'Добавить статью', 'urlname': 'add_post'},
    {'title': 'Обратная связь', 'urlname': 'contact'},
    {'title': 'Войти', 'urlname': 'login'},
]

stars_db = [
    {'id': 1,
     'title': 'Jackie Chan',
     'content': 'Biography ЧАНА',
     'published': True},
    {'id': 2,
     'title': 'Johny Depp',
     'content': 'Biography Депа',
     'published': False},
    {'id': 3,
     'title': 'Brat Pitt',
     'content': 'Biography Пита ',
     'published': True},
]


# Create your views here.
def index(request):
    new_data = Stars.objects.all()
    data = {'title': 'Звезды',
            'menu': menu,
            'stars_info': stars_db,
            'db_stars': new_data}
    return render(request, "index.html", data)


def about(request):
    data = {'title': 'О нас ', 'menu': menu}
    return render(request, "about.html", data)


def contact(request):
    return render(request, 'contact.html', {'menu': menu})

    # return HttpResponse("О нас")


@csrf_protect
def add_post(request):
    if request.method=='POST':
        first_name=request.POST.get('fname')
        last_name=request.POST.get('lname')
        title= f'{first_name} {last_name}'
        content=request.POST.get('content')
        category = request.POST.get('category')
        id=Category.objects.get(name=category).id
        if not id:
            return HttpResponse("<h1> Нет такой категории </h1> <a href='index.html>Вернутся</a>")
        Stars.objects.create(title = title,content=content,category_id=id).save()
        print(request.POST)
        print(f'{first_name}\n{last_name}\n{category}\n{content}\n{title}')

    return render(request, 'add_post.html', {'menu': menu})


def login(request):
    return render(request, 'login.html', {'menu': menu})


def create_new_category(request):
    return render(request, "create_new_category.html")


def categories(request, **kwargs):
    cat_id = kwargs.get('cat_id')
    if cat_id == 5:
        return create_new_category(request)
    data = Stars.objects.filter(category_id=cat_id)
    name = Category.objects.get(id=cat_id).name
    # name = kwargs.get('name', '')

    return render(request, "new_category.html", {'cat_id': cat_id, 'name': name, 'data': data})


def post(request, post_id):
    data = Stars.objects.get(id=post_id)
    # for person in stars_db:
    #     if person['id'] == post_id and person['published']:
    #         find = True
    #         break  # Нашли элемент, выходим из цикла
    if data:
        if data.is_published:
            return render(request, 'post.html', {'post': data.title, 'content': data.content})
    return render(request, 'post.html', {'post': 'Not Found', 'content': 'This post does not exist.'})

# def categories_by_slyg(request, cat_slug):
#     print(request.GET)
#     return HttpResponse(f"Cтатьи по категориям{cat_slug}")


# def error_page(request, exception=None, status_code=404):
#     return HttpResponse(f"<h1>Ошибка  {status_code}</h1>", status=status_code)
