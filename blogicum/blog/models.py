from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

MAX_LENGTH = 256


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH)
    description = models.TextField(_('Описание'))
    slug = models.SlugField(
        _('Идентификатор'),
        unique=True,
        help_text=_(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(_('Название места'), max_length=MAX_LENGTH)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH)
    text = models.TextField(
        _('Текст'),
        help_text=_('Введите текст публикации')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор публикации')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Местоположение')
    )
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        default_related_name = 'posts'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
