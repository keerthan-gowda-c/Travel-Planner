from django.shortcuts import render
import os
import re 
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics,status as http_status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from subscriptions.models import Subscription
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class GoogleSignInView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        token = request.data.get("credential")

        if not token:
            return Response({"detail":"Google credential is required."},status=http_status.HTTP_400_BAD_REQUEST)

        if not settings.GOOGLE_CLIENT_ID:
            return Response({"detail":"Google Sign-In is not configued on the server"},status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            google_user = id_token.verify_oauth2_token(token,google_requests.Request(),settings.GOOGLE_CLIENT_ID,)

        except ValueError:
            return Response({"detail":"Invalid Google token."},status=http_status.HTTP_401_UNAUTHORIZED)

        email = google_user.get("email","").strip().lower()
        email_verified = google_user.get("email_verified",False)
        full_name = google_user.get("name","").strip()

        if not email or not email_verified:
            return Response({"detail":"A verified Google email is required"},status=http_status.HTTP_400_BAD_REQUEST)


        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            base_username = email.split("@")[0]
            base_username = re.sub(r"[^a-zA-Z0-9_.@+-]","",base_username)
            base_username = base_username[:140] or "googleuser"
            username = base_username
            counter = 1

            while User.objects.filter(username=username).exists():
                suffix = str(counter)
                username = f"{base_username[:150-len(suffix)]}{suffix}"
                counter += 1

            name_parts = full_name.split(maxsplit=1)

            user = User.objects.create_user(username=username,email=email,first_name=name_parts[0] if name_parts else "",last_name=name_parts[1] if len(name_parts)>1 else "",)

        Subscription.objects.get_or_create(user=user,defaults={"plan":"free","status":"free"})

        refresh = RefreshToken.for_user(user)

        return Response({
            "message":"Google Sign-in successfull.",
            "access":str(refresh.access_token),
            "refresh":str(refresh),
            "user":{
                "id":str(user.pk),
                "username":user.username,
                "email":user.email,
                "full_name":user.get_full_name(),
            }
        })


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        subscription,_ = Subscription.objects.get_or_create(user=user, defaults={"plan":"free","status":"free"})

        return Response({
            "id": str(user.pk),
            "username": user.username,
            "email": user.email,
            "full_name": user.get_full_name(),
            "subscription": {
                "plan": subscription.plan,
                "status": subscription.status,
                "billing_period": subscription.billing_period,
            }
        }, status=http_status.HTTP_200_OK)