from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


# Create your models here.
class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_images/', default=None, blank=True, null=True,
                              verbose_name='Фото пользователя')
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
