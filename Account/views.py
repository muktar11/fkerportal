from django.shortcuts import render
from django.http import JsonResponse
from .models import Staff, WebCustomer, WebCustomerProfile
from serializer.serializers import StaffSerializer,  MyTokenObtainPairSerializer, RegisterStaffSerializer, WebCustomerSerializer, WebCustomerProfileSerialzier, ForgotPasswordSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics 
from .permissions import IsWebCustomerUser, IsStaffUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

def index(request):
    return render(request, 'index.html')



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.get_user(request.data['email'])  # Get the user based on the provided email

        if isinstance(user, Staff):
            response.data['role'] = user.role

        if isinstance(user, Staff):
            response.data['last_name'] = user.last_name

        if isinstance(user, Staff):
            response.data['first_name'] = user.first_name

        if isinstance(user, Staff):
            response.data['id'] = user.id


        return response

    def get_user(self, email):
        try:
            return Staff.objects.get(email=email)
        except Staff.DoesNotExist:
            return None
        
class RegisterStaffView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterStaffSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        # Generate the tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
      

        # Return the response with user credentials and access token
        return Response({
            'message': 'User registered successfully',
            'user': RegisterStaffSerializer(user).data,
            'access_token': access_token,
            
        })


@api_view(['GET'])
def get_profiles(request):
    queryset = Staff.objects.all()
    serializer = StaffSerializer(queryset,many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def get_profile(request, pk):
    queryset = Staff.objects.filter(id=pk)
    serializer = StaffSerializer(queryset,many=True, context={'request': request})
    return Response(serializer.data)



@api_view(['PUT'])
def update_profile(request, pk):
    data = request.data
    staff = Staff.objects.get(id=pk)
    
    if 'email' in data:
        staff.email = data['email']
    if 'first_name' in data:
        staff.first_name = data['first_name']
    if 'last_name' in data:
        staff.last_name = data['last_name']
    if 'image' in data:
        staff.image = data['image']
    if 'role' in data:
        staff.role = data['role']
    if 'password' in data and data['password'] != '':
        staff.set_password(data['password'])
    
    staff.save()
    serializer = StaffSerializer(staff, context={'request': request})
    return Response(serializer.data)
@api_view(['GET'])
def access_staff(request):
    queryset = Staff.objects.all()
    serializer = StaffSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

class WebCustomerCreateView(generics.CreateAPIView):
    queryset = WebCustomer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = WebCustomerSerializer 

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        serializer.save(password=password)

@api_view(['POST'])
def approve_web_customer(request, _id):
    customer = WebCustomer.objects.get(_id=_id)
    customer.is_approved = True
    customer.save()
    serializer = WebCustomerSerializer(customer, context={'request': request})
    return Response(serializer.data)
        

@api_view(['GET'])
def retrieve_not_approved_customers(request):
    not_approved_customers = WebCustomer.objects.filter(is_approved=False)
    serializer = WebCustomerSerializer(not_approved_customers, many=True, context={'request': request})
    return Response(serializer.data)




@api_view(['GET'])
def retrieve_approved_customers(request):
    approved_customers = WebCustomer.objects.filter(is_approved=True)
    serializer = WebCustomerSerializer(approved_customers, many=True, context={'request': request})
    return Response(serializer.data)

class WebCustomerListView(generics.ListAPIView):
    queryset = WebCustomer.objects.all()
    permission_classes = [AllowAny]
    serializer_class = WebCustomerSerializer


class WebCustomerEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = WebCustomerProfile.objects.all()
    permission_classes  = (AllowAny)
    serializer_class = WebCustomerProfileSerialzier 


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset token sent successfully."})