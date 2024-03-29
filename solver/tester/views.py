from django.shortcuts import render, HttpResponse


# Create your views here.
def main(request):
    return HttpResponse('<h1>Здесь совсем скоро будет главная страница сайта)</h1>')
