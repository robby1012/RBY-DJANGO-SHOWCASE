import datetime

from django.utils import timezone
from rest_framework.serializers import ModelSerializer, BooleanField

from library.models import BookLog


class LendingOrReturnSerializer(ModelSerializer):
    is_cancel = BooleanField()

    class Meta:
        model = BookLog
        fields = (
            'is_cancel',
        )

    def validate(self, attrs):
        # check the book log if it status inquiry or not
        if self.instance.status == BookLog.Status.INQUIRY:
            attrs['status'] = BookLog.Status.LEASED if 'is_cancel' not in attrs or not attrs[
                'is_cancel'] else BookLog.Status.CANCEL

        elif self.instance.status == BookLog.Status.LEASED:
            # get latest modified time
            lend_deadline = self.instance.updated_at + datetime.timedelta(days=30)

            attrs['status'] = BookLog.Status.RETURN if lend_deadline >= timezone.now() else BookLog.Status.OVERDUE
        return attrs

    def update(self, instance, validated_data):
        """
        Modified create process on serialization

        Args:
            validated_data: filter parameter from validation process

        Returns:
            Instance object from model Users
        """
        instance.status = validated_data['status']
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Override object represented for return serializer

        Args:
            instance: model instance to be represented

        Returns:
            Dictionary object from represented instance
        """
        return {
            'uuid'      : instance.uuid,
            'title'     : instance.book.title,
            'author'    : instance.book.author,
            'publish'   : instance.book.publish,
            'price'     : instance.book.price,
            'copies'    : instance.copies,
            'status'    : instance.status,
        }