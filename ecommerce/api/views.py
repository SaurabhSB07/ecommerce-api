from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import (
    UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserChangePasswordSerializer, UserChagePasswordResetEmailSerializer, UserPasswordResetSerializer
)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterationView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registration Successful', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class UserLoginView(APIView):
    permission_classes = []
    def post(self, request): 
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, "msg": 'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=200)

class UserChagePasswordResetEmailRequestView(APIView):      # Forgaot password endpoint: gets email, sends link
    permission_classes = []
    def post(self, request):
        serializer = UserChagePasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg": "Password reset link is sent to your email. Please check your inbox."})

class UserPasswordResetView(APIView):                       # Handles reset link (uid, token in URL)
    permission_classes = []
    def post(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
