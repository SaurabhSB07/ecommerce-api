from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status,viewsets,permissions
from .models import Product,Cart,CartItem,Order,OrderItem,Review
from django.contrib.auth import authenticate
from .serializers import (
    UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserChangePasswordSerializer, UserChagePasswordResetEmailSerializer, UserPasswordResetSerializer
)
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer,OrderItemSerializer,OrderSerializer,ReviewSerializer
from rest_framework import filters




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

###########################################################

class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends = [filters.SearchFilter]   #searchfilter for product
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()] 
###############################################################
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Cart.objects.all()  # Admin sees all carts
        return Cart.objects.filter(user=user)  # fro normal users see only their carts

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-assign cart to logged in user


class CartItemView(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)  # Only user's cart items

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart:
            cart = Cart.objects.create(user=self.request.user)  # Create cart if none exists
        serializer.save(cart=cart)  # Automatically link CartItem to the user's cart   
#####################################################################

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # showing user's orders

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-attach the current user

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class=OrderItemSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)  
####################################################################################  
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all() #when hit get , user will get to see all review below the product
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)#for posting his own review , auto attached curr. user name 
