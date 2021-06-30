from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import (
    ProfileSerializer,
    UserSerializer,
    PopulatedProfileSerializer
)

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'detail': 'Unauthorized'})

        expiry_time = datetime.now() + timedelta(days=3)

        token = jwt.encode(
            {'sub': str(user_to_login.id), 'user': str(user_to_login.username), 'exp': int(
                expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response(data={
            'token': token,
            'message': f'Welcome back {user_to_login.username}'},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, _request, pk):
        user = User.objects.get(pk=pk)
        serializedUser = PopulatedProfileSerializer(user)
        return Response(data=serializedUser.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)

        user_to_modify = ProfileSerializer(user, data=request.data)

        if user_to_modify.is_valid():
            user_to_modify.save()
            return Response(data=user_to_modify.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=user_to_modify.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class FollowUser(APIView):
    def post(self, _request, userId, followId):
        try:
            print(userId)
            print(followId)
            user = User.objects.get(pk=userId)
            follow = User.objects.get(pk=followId)
            if follow in user.followers.all():
                user.followers.remove(followId)
            else:
                user.followers.add(followId)
            user.save()
            user_who_followed = PopulatedProfileSerializer(user)
            return Response(data=user_who_followed.data, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            raise NotFound()
