from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(_('title'), max_length=50)
    sku = models.CharField(_('stock keeping unit'), max_length=20, validators=[validate_sku])
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='packages/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    price = models.PositiveIntegerField(_('price'))
    durations = models.DurationField(_('duration'), blank=True, null=True)
    # getmays = models.ManyToManyField('payments.Gateway')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now_add=True)

    class Meta:
        db_table = _('packages')
        verbose_name = _('package')
        verbose_name_plural = _('package')

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.CharField('users.User', max_length=50)
    package = models.ForeignKey(Package, related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'), blank=True, null=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
