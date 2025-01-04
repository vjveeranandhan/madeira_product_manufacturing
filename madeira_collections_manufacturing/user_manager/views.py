from django.shortcuts import render
from . user_data_validation import validate_user_data
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializer import UserSerializer, LoginSerializer, UserRetrieveSerializer, CustomUserSerializer
from .models import CustomUser
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

# Create your views here.

def send_custom_mail(user_email):
    subject = 'Tourneyhub'
    message = 'Welcome to Tourneyhub!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    try:
        django_send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user(request):
    print("create_user")
    # return Response({'message': 'user created'}, status= status.HTTP_201_CREATED)
    try:
        if request.method == 'POST':
            validation_check_status = validate_user_data(request.data, 'user-creation')
            print("validation_check_status", validation_check_status)
            if validation_check_status[0] ==  False:
                check_status_response = validation_check_status[1]
                return Response({"message":check_status_response}, status=status.HTTP_406_NOT_ACCEPTABLE)
            _data = request.data
            serializer = UserSerializer(data= _data, many = False)
            print(serializer)
            if serializer.is_valid():
                user = CustomUser.objects.create(name= serializer.validated_data['name'], email = serializer.validated_data['email'],
                                                phone = serializer.validated_data['phone'], age= serializer.validated_data['age'],
                                                isAdmin = serializer.validated_data['isAdmin'], username=serializer.validated_data['name'],)
                user.set_password(_data['password'])
                user.save()
                # send_custom_mail(serializer.validated_data['email'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if user:
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid user id'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_view(request):
    try:
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not phone or not password:
            return Response({'error': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = CustomUser.objects.get(phone=phone) 
        if user is None:
            return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'isAdmin': user.isAdmin
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Optional: Require the user to be authenticated
def get_all_users(request):
    try:
        print("inside user")
        users = CustomUser.objects.all()  # Get all users
        serializer = CustomUserSerializer(users, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_user_by_id(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        # You can serialize the user data if needed, for now returning raw data
        data = {
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'isAdmin': user.isAdmin,
        }
        return Response(data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
