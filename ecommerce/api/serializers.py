from rest_framework import serializers
from .models import User,Product,Cart,CartItem,Order,OrderItem,Review
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'tc', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'tc': {'required': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Passwords do not match'})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
    'profile_image',
    'name',
    'email',
    'gender',
    'date_of_birth',
    'phone',
    'address_line1',
    'address_line2',
    'city',
    'state',
    'country',
    'postal_code',
]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    def validate(self, attrs):
        user = self.context.get('user')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password fields did not match")
        user.set_password(password)
        user.save()
        return attrs

class UserChagePasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get('email')
        from django.core.mail import send_mail
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:8000/api/reset-password/{uid}/{token}/'
            # For development: printing the link
            print("Reset link:", link)
            # In real time we config django to use SMTP settings for Gmail,etc  , its shown below line
            # send_mail('Password Reset Link', f'Your reset link: {link}', 'noreply@yourdomain.com', [email])
            return attrs
        raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid or expired reset link')
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Token is not valid or expired')
        user.set_password(password)
        user.save()
        return attrs
#####################################################
class ReviewSerializer(serializers.ModelSerializer):
    customer_name=serializers.ReadOnlyField(source='user.name')
    class Meta:
        model=Review
        fields=["customer_name",'rating','description']
        read_only_fields = ["user"]
#--------------------------------------------------------------#
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model=Product 
        exclude = ['created_at', 'is_active']   
###################################################### 
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name') # Show product name in API
    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity","cart"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nest cart items inside cart response
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Cart
        fields = ["id", "user", "items","user_email"]
        read_only_fields = ["user"]
######################################################
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order 
        exclude=["created_at"]      
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_name", "quantity", "price_at_purchase"]
        product_name = serializers.ReadOnlyField(source="product.name")
######################################################################### 




      