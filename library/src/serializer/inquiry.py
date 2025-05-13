from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField, IntegerField

from library.models import BookLog, Book


class InquiryCreateSerializer(ModelSerializer):
    uuid   = CharField(write_only=True)
    copies = IntegerField(write_only=True)

    class Meta:
        model = BookLog
        fields = (
            'uuid',
            'copies',
        )

    def validate(self, attrs):
        # get all the book uuid and number of copies that been held and then calculate with number of stocks copies
        book_copies_held = 0
        book_leased      = BookLog.objects.filter(book=attrs['uuid'], status__in=(BookLog.Status.LEASED, ))
        for i in book_leased:
            book_copies_held += i.copies

        book_lists        = get_object_or_404(Book, uuid=attrs['uuid'])
        book_copies_avail = book_lists.copies - book_copies_held

        if attrs['copies'] > book_copies_avail:
            raise ValidationError('Inquiry copies is exceeding with stocks copies')

        attrs['book'] = book_lists

        return attrs

    def create(self, validated_data):
        """
        Modified create process on serialization

        Args:
            validated_data: filter parameter from validation process

        Returns:
            Instance object from model Users
        """
        del validated_data['uuid']

        validated_data['user']   = self.context.get("request").user
        validated_data['status'] = BookLog.Status.INQUIRY

        instance = super().create(validated_data)
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
            'copies'    : instance.copies
        }


class InquiryUpdateSerializer(ModelSerializer):
    copies = IntegerField(write_only=True)

    class Meta:
        model = BookLog
        fields = (
            'copies',
        )

    def validate(self, attrs):
        # get all the book uuid and number of copies that been held and then calculate with number of stocks copies
        book_copies_held = 0
        book_leased      = BookLog.objects.filter(book=self.instance.book.uuid, status__in=(BookLog.Status.LEASED, ))
        for i in book_leased:
            book_copies_held += i.copies

        book_lists        = get_object_or_404(Book, uuid=self.instance.book.uuid)
        book_copies_avail = book_lists.copies - book_copies_held

        if attrs['copies'] > book_copies_avail:
            raise ValidationError('Inquiry copies is exceeding with stocks copies')

        return attrs

    def update(self, instance, validated_data):
        """
        Modified create process on serialization

        Args:
            validated_data: filter parameter from validation process

        Returns:
            Instance object from model Users
        """
        instance.copies = validated_data['copies']
        instance.status = BookLog.Status.INQUIRY
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
            'copies'    : instance.copies
        }