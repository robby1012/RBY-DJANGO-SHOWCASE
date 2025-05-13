from uuid import uuid4

from django.conf import settings
from django.db import models as _


# ____model abstract for pre-usage in model class____
class AbstractUUIDModel(_.Model):
    class Meta:
        abstract = True

    uuid = _.UUIDField(primary_key=True, default=uuid4, editable=False)

    def __str__(self):
        return str(self.uuid)


# ____model abstract for auditing in model class___
class AbstractAuditModel(AbstractUUIDModel):
    class Meta:
        abstract = True

    created_by = _.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=_.SET_NULL, related_name='%(class)s_created_by'
    )
    created_at = _.DateTimeField(auto_now_add=True)
    updated_by = _.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=_.SET_NULL, related_name='%(class)s_modified_by'
    )
    updated_at = _.DateTimeField(auto_now=True)
