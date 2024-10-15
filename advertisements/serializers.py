from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', 'updated_at')
        read_only_fields = ('creator', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания объявления."""

        # Автоматическое проставление создателя объявления.
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context['request'].user.advertisement_set.filter(status='OPEN').count() >= 10:
            raise serializers.ValidationError('Вы не можете иметь больше 10 открытых объявлений.')

        return data