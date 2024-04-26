from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.

class Test(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 0, 'Открытое'
        PRIVATE = 1, 'Приватное'

    title = models.CharField(verbose_name='Название', max_length=101)
    content = models.JSONField(blank=True, null=True, default=None)
    counter = models.IntegerField(verbose_name='Число решений', default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='test',
                               default=None)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='test', verbose_name='Категория',
                                 default=None, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, related_name='test', default=None,
                                verbose_name='Предмет', null=True)
    status = models.BooleanField(verbose_name='Статус', default=Status.PRIVATE,
                                 choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)))

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_edit = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def get_absolute_url(self):
        return reverse('test', kwargs={'test_id': self.pk})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)

    # slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def get_absolute_url(self):
        return reverse('subject', kwargs={'subject_id': self.pk})

    def __str__(self):
        return self.name


class Result(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест', related_name='results')
    result = models.JSONField(blank=True, null=True, default=None, verbose_name='Ответы')
    numbers_of_correct = models.IntegerField(verbose_name='Число верных')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def get_absolute_url(self):
        return reverse('result', kwargs={'result_id': self.pk})

    def __str__(self):
        return f'Result: user:{self.user.username}, test: {self.test.pk}, when: {self.time_create}'
