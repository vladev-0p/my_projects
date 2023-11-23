from django.shortcuts import render

# Create your views here.

def index(request): #информация о запросе
    return render(request,'core/index.html')