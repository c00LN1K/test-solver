from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    name = models.CharField(verbose_name='Имя пользователя', blank=True, max_length=33)
    photo = models.ImageField(upload_to='profile_images/', default=None, blank=True, null=True,
                              verbose_name='Фото пользователя')
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


class Test(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 0, 'Открытое'
        PRIVATE = 1, 'Приватное'

    title = models.CharField(verbose_name='Название', max_length=100)
    content = models.JSONField()
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
