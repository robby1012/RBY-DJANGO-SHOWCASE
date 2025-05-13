from django.db import models as _
from django.contrib.auth.models import User


class Profile(_.Model):
    user    = _.OneToOneField(User, on_delete=_.CASCADE)
    address = _.TextField(null=True, blank=True)
    phone   = _.CharField(max_length=25)

    class Meta:
        verbose_name        = 'User profile'
        verbose_name_plural = 'User profiles'
