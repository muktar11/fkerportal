from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Staff, WebCustomer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.http import JsonResponse

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'role')

class WebCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebCustomer
        fields = ('id', 'email', 'customer_name', 'sales_route', 'tin_number', 'business_license_no', 'business_registration_no', 'sales_target', 'gps_coordinates')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Custom claims for Staff users
        if isinstance(user, Staff):
            token['role'] = user.role
        
        # Custom claims for WebCustomer users
        if isinstance(user, WebCustomer):
            token['customer_name'] = user.customer_name
        
        # Add more custom claims as needed
        # ...
        
        return token
 
class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Staff
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Staff.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class RegisterWebCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = WebCustomer
        fields = ('email', 'customer_name', 'password', 'password2', 'sales_route', 'tin_number', 'business_license_no', 'business_registration_no', 'sales_target', 'gps_coordinates')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        # Create the user
        user = WebCustomer.objects.create(
            email=validated_data['email'],
            customer_name=validated_data['customer_name'],
            sales_route=validated_data['sales_route'],
            tin_number=validated_data['tin_number'],
            business_license_no=validated_data['business_license_no'],
            business_registration_no=validated_data['business_registration_no'],
            sales_target=validated_data['sales_target'],
            gps_coordinates=validated_data['gps_coordinates']
        ) 
        # Set the password and save the user
        user.set_password(validated_data['password'])
        user.save()

        # Generate the tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the serialized user with the access token
        return {
            'message': 'User registered successfully',
            'user': WebCustomerSerializer(user).data,
            'access_token': access_token
        }
    
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random
import string

User = get_user_model()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate a random password reset token
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Update the user's password reset token field
        user.password_reset_token = token
        user.save()

        # Send password reset email with token
        send_mail(
            'Password Reset',
            f'Your password reset token is: {token}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return user