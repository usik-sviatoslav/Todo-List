from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import CharField, ModelSerializer, ValidationError

from apps.user.models import User


class SignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "password2", "refresh", "access"]

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)
    refresh = CharField(read_only=True)
    access = CharField(read_only=True)

    def validate(self, attrs: dict):
        password = attrs.get("password")
        password2 = attrs.pop("password2")

        if password == password2:
            return attrs

        raise ValidationError({"password": "Password fields didn't match."})

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["username"] = validated_data["email"].split("@")[0]
        return super().create(validated_data)
