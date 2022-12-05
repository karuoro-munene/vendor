from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    username = serializers.CharField(
        required=True,
        max_length=50,
    )
    password = serializers.CharField(
        required=True,
        max_length=16,
    )
    role = serializers.CharField(
        required=True
    )

    def create(self, validated_data):
        account = get_user_model().objects.create_user(
            role=validated_data["role"],
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return account

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    class Meta(object):
        model = get_user_model()
        fields = ("email", "username", "email", "role", "password")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
