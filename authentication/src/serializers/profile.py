from rest_framework.serializers import ModelSerializer, ImageField

from authentication.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "address",
            "phone"
        )

    def create(self, validated_data):
        """
        Modified create process on serialization

        Args:
            validated_data: filter parameter from validation process

        Returns:
            Instance object from model Users
        """
        validated_data["user"] = self.context.get("request").user
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
            "phone": instance.phone,
            "address": instance.address
        }