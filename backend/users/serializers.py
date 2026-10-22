
from django.contrib.auth.models import User
from rest_framework import serializers
import re


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8, max_length=16)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "email", "password"]

    def validate_password(self,value):
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,16}",value):
            raise serializers.ValidationError(
                "Password must be 8-16 characters, uppercase, lowercase, number and special characters"
            )
        return value

    def create(self, validated_data):
        full_name = validated_data.pop("full_name").split(maxsplit=1)

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=full_name[0],
            last_name=full_name[1] if len(full_name) > 1 else ""
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["full_name"] = instance.get_full_name()
        return data
