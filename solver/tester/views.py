from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache, caches
from django.http import Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView
from django_redis import get_redis_connection

from .models import Test, Result

DEFAULT_TTL = 10


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
        duration = int(request.POST.get('duration', DEFAULT_TTL)) * 60
        if user in cache:
            messages.add_message(request, messages.ERROR,
                                 'Вы уже проходите тест. Сначала завершите его перед началом нового')
            test_id = cache.get(user)['test_id']
        else:
            test = get_test_content(test_id, duration)
            data = dict.fromkeys(test.keys(), None)
            data['test_id'] = test_id
            # TODO: timer and automatic finish (redirect) after expiration of time
            cache.set(user, data, duration)
        return redirect(reverse('question', kwargs={'test_id': test_id, 'question_id': 1}))
    elif request.method == 'GET':
        obj = Test.objects.filter(pk=test_id).first()  # status=Test.Status.OPEN
        if not (obj and (not obj.status or (obj.status and obj.author == request.user))):
            raise Http404()
        return render(request, 'tester/start_test.html', context={'title': 'Решить тест', 'test': obj})


def get_test_content(test_id, duration=60 * 10 + 10) -> dict:
    test_key = f'test_{test_id}'
    if test_key in cache:
        test = cache.get(test_key)
    else:
        test = get_object_or_404(Test, pk=test_id)
        cache.set(test_key, test.content, duration)
        test = test.content
    return test


@login_required()
def get_question(request, test_id, question_id):
    user = f'user_{request.user.pk}'
    if user not in cache or cache.get(user)['test_id'] != test_id:
        raise Http404()
    test = get_test_content(test_id)
    if request.method == 'POST':
        choice = request.POST['choice']
        user_ans = cache.get(user)
        user_ans[str(question_id)] = choice
        ttl = cache.ttl(user)
        cache.set(user, user_ans, ttl)
        action = int(request.POST['action'])
        if action:
            return redirect(reverse('question', kwargs={'test_id': test_id, 'question_id': question_id + action}))
        return finish_test(request, test_id)

    prev_question = next_question = 0
    if question_id > 1:
        prev_question = question_id - 1
    if len(test) > question_id:
        next_question = question_id + 1
    marked = -1
    if el := cache.get(user)[str(question_id)]:
        marked = el
    return render(request, 'tester/question.html',
                  context={'data': test[str(question_id)], 'title': f'Вопрос {question_id}', 'prev': prev_question,
                           'next': next_question, 'marked': marked})


def get_number_correct(data: dict, test: dict):
    res = 0
    for question, answer in data.items():
        if question != 'test_id':
            if test[question]['correct'] == answer:
                res += 1
    return res


def finish_test(request, test_id):
    user_key = f'user_{request.user.pk}'
    data = cache.get(user_key)
    user = request.user
    test = Test.objects.get(pk=test_id)
    result_id = Result.objects.create(user=user, test=test, result=data,
                                      numbers_of_correct=get_number_correct(data, test.content))
    cache.delete(user_key)
    print(cache.ttl(f'test_{test_id}'))
    return redirect(reverse('result', kwargs={'user_id': user.pk, 'result_id': result_id}))


class ShowResult(LoginRequiredMixin, DetailView):
    context_object_name = 'result'
    template_name = 'tester/result.html'
    pk_url_kwarg = 'result_id'
    extra_context = {'title': 'Результат'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = context['result'].time_create.strftime('%d.%m.%Y - %H:%M')
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Result, pk=self.kwargs[self.pk_url_kwarg])
