from django.urls import reverse_lazy


def get_menu(request):
    return {
        'menu': {
            'Главная страница': reverse_lazy('main'),
            'Добавить тест': reverse_lazy('add_test')
        }
    }
