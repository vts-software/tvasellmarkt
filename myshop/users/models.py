from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # <--- меняем related_name
        blank=True,
        help_text='Группы пользователя',
        verbose_name='группы'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # <--- меняем related_name
        blank=True,
        help_text='Разрешения пользователя',
        verbose_name='разрешения'
    )