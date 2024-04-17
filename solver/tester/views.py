from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView

from .models import Test


# Create your views here.
def main(request):
    return render(request, 'tester/main.html', context={'title': 'Главная страница'})


def parse_test(d: dict):
    # TODO: Ограничение на количество вопросов в тесте (максимальное и минимальное количество - на стороне браузера)
    data = {}
    del d['csrfmiddlewaretoken']
    del d['title']
    for key, val in d.items():
        if key.startswith('question'):
            key = int(key.split('-')[1])
            data[key] = data.setdefault(key, {})
            data[key]['question'] = val[0]
        elif key.startswith('answer'):
            q, a = key.split('-')[1:]
            q = int(q)
            data[q] = data.setdefault(q, {})
            data[q]['answers'] = data[q].setdefault('answers', {})
            data[q]['answers'][f'ans{a}'] = val[0]

        elif key.startswith('correct'):
            q = int(key.split('-')[1])
            data[q] = data.setdefault(q, {})
            data[q]['correct'] = f'ans{val[0]}'
    clear_data = {}
    for before, after in zip(data, range(1, len(d) + 1)):
        clear_data[after] = data[before]
    # for question in data.keys():
    #     if 'correct' not in data[question]:
    #         print(data)
    #         print(data[question])
    #         return {}

    return clear_data


@login_required()
def add_test(request):
    # TODO: Доработать форму добавления вопросов
    # когда добавляешь три варианта, удаляешь второй, добавляешь четвертый (третий по счету),
    # а он не отображается в request - ошибка в логике построения добавления ответов
    if request.method == 'POST':
        if request.POST:
            data = parse_test(dict(request.POST))
            print(data)
            if data:
                Test.objects.create(title=request.POST['title'], content=data, author=request.user)
                messages.add_message(request, messages.SUCCESS, "Тест успешно создан")
                return redirect(reverse('main'))
            else:
                messages.add_message(request, messages.ERROR, "Ошибка при создании")
    return render(request, 'tester/add_test.html')


class GetTest(LoginRequiredMixin, DetailView):
    template_name = 'tester/start_test.html'
    pk_url_kwarg = 'test_id'
    context_object_name = 'test'
    extra_context = {'title': 'Начать тест'}

    # сделать POST - начало теста, GET - получить тест


@login_required()
def start_test(request, test_id):
    if request.method == 'POST':
        user = f'user_{request.user.pk}'
        duration = request.POST.get('duration', 60 * 10)
        if user in cache:
            messages.add_message(request, messages.ERROR,
                                 'Вы уже проходите тест. Сначала завершите его перед началом нового')
            test_id = cache.get(user)['test_id']
        else:
            test_key = f'test_{test_id}'
            test = get_test_from_cache(test_key, test_id, duration)
            data = dict.fromkeys(test.content.keys(), None)
            data['test_id'] = test_id
            # TODO: timer and automatic finish (redirect) after expiration of time
            cache.set(user, data, duration)
        return redirect(reverse('question', kwargs={'test_id': test_id, 'question_id': 1}))
    elif request.method == 'GET':
        obj = Test.objects.filter(pk=test_id).first()  # status=Test.Status.OPEN
        if not (obj and (not obj.status or (obj.status and obj.author == request.user))):
            raise Http404()
        return render(request, 'tester/start_test.html', context={'title': 'Решить тест', 'test': obj})


def get_test_from_cache(test_key, test_id, duration=60 * 10) -> Test:
    if test_key in cache:
        test = cache.get(test_key)
    else:
        test = get_object_or_404(Test, pk=test_id)
        cache.set(test_key, test.content, duration)
    return test


@login_required()
def get_question(request, test_id, question_id):
    user = f'user_{request.user.pk}'
    if user not in cache or cache.get('user')['test_id'] != test_id:
        raise Http404()
    test_key = f'test_{test_id}'
    test = get_test_from_cache(test_key, test_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        user_ans = cache.get(user)
        user_ans[question_id] = choice  # may be error
        cache.set(user, user_ans, cache.ttl(user))  # may be error (if ttl not exists)

    return render(request, 'tester/question.html',
                  context={'data': test.content[question_id], 'title': f'Вопрос {question_id}'})


@login_required()
def finish_test(request, test_id):
    # check answers of users and show total
    pass
