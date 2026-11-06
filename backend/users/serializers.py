
from django.contrib.auth.models import User
from rest_framework import serializers
import re
from subscriptions.models import Subscription
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
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

        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
                first_name=full_name[0],
                last_name=full_name[1] if len(full_name) > 1 else ""
            )

        Subscription.objects.create(user=user,plan="free",status="free")

        return user 
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["full_name"] = instance.get_full_name()
        return data


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields.pop(self.username_field, None)

    def validate(self, attrs):
        User = get_user_model()
        email = attrs["email"]
        password = attrs["password"]
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            raise AuthenticationFailed("Invalid email or password")

        return super().validate({
            self.username_field: user.get_username(),
            "password": password,
        })
