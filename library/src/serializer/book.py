from rest_framework.serializers import ModelSerializer, CharField, IntegerField, DecimalField

from library.models import Book


class BookSerializer(ModelSerializer):
    title    = CharField(write_only=True)
    synopsis = CharField(write_only=True)
    publish  = IntegerField(write_only=True)
    author   = CharField(write_only=True)
    price    = DecimalField(write_only=True, max_digits=8, decimal_places=0)
    copies   = IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = (
            'title',
            'synopsis',
            'publish',
            'author',
            'price',
            'copies'
        )

    def create(self, validated_data):
        """
        Modified create process on serialization

        Args:
            validated_data: filter parameter from validation process

        Returns:
            Instance object from model Users
        """
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
            'full_title': f'{instance.title} by {instance.author} ',
            'title'     : instance.title,
            'author'    : instance.author,
            'publish'   : instance.publish,
            'price'     : instance.price,
            'synopsis'  : instance.synopsis,
            'copies'    : instance.copies
        }
