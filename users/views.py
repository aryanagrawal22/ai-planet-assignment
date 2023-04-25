from rest_framework.decorators import api_view
from rest_framework.response import Response
from cerberus import Validator
from rest_framework import status
from users.models import User
from utility.encrytionHelper import EncryptionHelper
from utility.authMiddleware import is_authenticated
from hackathons.models import HackathonRegister
from users.serializers import UserSerializer

@api_view(['POST'])
def register(request):
    try:
        schema = {
            "name": {'type': 'string', 'required': True, 'empty': False},
            "email": {'type': 'string', 'required': True, 'empty': False },
            "password": {'type': 'string', 'required': True, 'empty': False },
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response({'error': v.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')
        
        # if account is already active
        if User.objects.filter(email=email).exists():
            return Response({'error': "EMAIL_NUMBER_ALREADY_EXIST"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create(
                    name=name,
                    email=email,
                    password=password,
                )
        return Response({'message': "USER_REGISTER"}, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def login(request):
    try:
        schema = {
            "email": {'type': 'string', 'required': True, 'empty': False },
            "password": {'type': 'string', 'required': True, 'empty': False },
        }
        v = Validator()
        if not v.validate(request.data, schema):
            return Response({'error': v.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        password = request.data.get('password')
        
        if not User.objects.filter(email=email).exists():
            return Response({'error': "NOT_REGISTERED"}, status=status.HTTP_400_BAD_REQUEST)
        
        user=User.objects.get(email = email)
        
        if(password!=user.password):
            return Response({'error': "INCORRECT_PASSWORD"}, status=status.HTTP_400_BAD_REQUEST)
        
        encryption_obj = EncryptionHelper(user.user_id)
        
        access_token = encryption_obj.create_access_token()
        response = dict({'user_id': user.user_id})
        response.update({'access_token': access_token})

        return Response(response, status=status.HTTP_200_OK)
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@is_authenticated
def check_profile(request):
    return Response(str(request.user))


# LOGIC: Get registerd users list and then check in users table if it exists in the list to get atleast 1 registered user
@api_view(['GET'])
@is_authenticated
def get_atleast_one_registered_users(request):
    try:
        registered_users = HackathonRegister.objects.all().values_list('user', flat=True)
        user = User.objects.filter(user_id__in=registered_users).order_by("-created_at")
        response = UserSerializer(user, many=True).data
        return Response(response, status=status.HTTP_200_OK)
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)