from django.contrib.auth.models import User
from django.db import models as _
from django.utils.translation import gettext_lazy as _lazy

from simplelib.src import AbstractAuditModel


# Create your models here.
class Book(AbstractAuditModel):
    title    = _.CharField(max_length=199)
    synopsis = _.TextField()
    price    = _.DecimalField(max_digits=8, decimal_places=0)
    publish  = _.IntegerField()
    author   = _.CharField(max_length=199)
    copies   = _.IntegerField()

    class Meta:
        verbose_name        = 'Book'
        verbose_name_plural = 'Books'
        ordering            = ['-created_at']


class BookLog(AbstractAuditModel):
    class Status(_.TextChoices):
        INQUIRY = 'IQ', _lazy('Inquiry')
        LEASED  = 'LD', _lazy('Leased')
        RETURN  = 'RT', _lazy('Return')
        CANCEL  = 'CL', _lazy('Cancel')
        OVERDUE = 'OD', _lazy('Overdue')

    user   = _.ForeignKey(User, on_delete=_.CASCADE)
    book   = _.ForeignKey(Book, on_delete=_.CASCADE)
    status = _.CharField(max_length=2, choices=Status, default=Status.INQUIRY)
    copies = _.IntegerField()

    class Meta:
        verbose_name        = 'Log book'
        verbose_name_plural = 'Log books'
        ordering            = ['-created_at']


class BookDamaged(AbstractAuditModel):
    log               = _.ForeignKey(BookLog, on_delete=_.SET_NULL, null=True)
    compensation_paid = _.BooleanField(default=False)
    copies            = _.IntegerField()

    class Meta:
        verbose_name        = 'Damaged'
        verbose_name_plural = 'Damaged books'
        ordering            = ['-created_at']
