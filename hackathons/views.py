from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hackathons.models import Hackathon, HackathonRegister
from utility.authMiddleware import is_authenticated
import datetime
from django.db.models import Q
from hackathons.serializers import HackathonSerializer
from pytz import UTC

@api_view(['POST'])
@is_authenticated
def create(request):
    try:
        user = request.user
        
        if not user.is_staff:
            return Response({'error': "User not authorised"}, status=status.HTTP_400_BAD_REQUEST)
        
        title = request.data.get('title')
        if Hackathon.objects.filter(title=title).exists():
            return Response({'error': "Hackathon with similar title alreeady exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        start_time = datetime.datetime.strptime(start_time, '%y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%y-%m-%d %H:%M:%S')
        print(start_time, end_time)
        
        if end_time<datetime.datetime.now():
            return Response({'error': "End date cannot be before today"}, status=status.HTTP_400_BAD_REQUEST)
        
        if end_time<start_time:
            return Response({'error': "end_time cannot be less then start_time"}, status=status.HTTP_400_BAD_REQUEST)
        
        description = request.data.get('description', None)
        background_image = request.data.get('background_image', None)
        hackathon_image = request.data.get('hackathon_image', None)
        reward_prize = request.data.get('reward_prize', None)
        
        Hackathon.objects.create(
                    title=title,
                    description=description,
                    hackathon_image=hackathon_image,
                    background_image=background_image,
                    reward_prize=reward_prize,
                    start_time=start_time,
                    end_time=end_time,
                )
        return Response({'message': "HACKATHON_CREATED"}, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
@is_authenticated
def get_hackathons(request):
    try:
        # Filters are: ALL (Default), FINISHED, ONGOING, INCOMING
        filter = (request.query_params.get("filter", "all")).lower()
        
        if filter=="finished":
            hackathons = Hackathon.objects.filter(end_time__lte=datetime.datetime.now()).order_by("start_time")
        elif filter=="ongoing":
            hackathons = Hackathon.objects.filter(Q(Q(start_time__lte=datetime.datetime.now()) & Q(end_time__gte=datetime.datetime.now()))).order_by("start_time")
        elif filter=="incoming":
            hackathons = Hackathon.objects.filter(Q(Q(start_time__gte=datetime.datetime.now()) & Q(end_time__gte=datetime.datetime.now()))).order_by("start_time")
        else:
            hackathons = Hackathon.objects.filter().order_by("start_time")
            
        response = HackathonSerializer(hackathons, many=True).data
        return Response(response, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@is_authenticated
def hackathon_register(request):
    try:
        user = request.user
        hackathon_id = request.data.get('hackathon_id')
        
        if hackathon_id is None:
            return Response({'error': "hackathon_id is needed to register"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Hackathon.objects.filter(id=hackathon_id).exists():
            return Response({'error': "hackathon_id is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        
        if hackathon.end_time<datetime.datetime.now().replace(tzinfo=UTC):
            return Response({'error': "Hackathon has ended"}, status=status.HTTP_400_BAD_REQUEST)
        
        if HackathonRegister.objects.filter(Q(Q(user=user)&Q(hackathon=hackathon))).exists():
            return Response({'error': "User already registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        HackathonRegister.objects.create(
                    user=user,
                    hackathon=hackathon
                )
        return Response({'message': "USER REGISTERED FOR HACKATHON"}, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@is_authenticated
def get_registered_hackathons(request):
    try:
        user = request.user
        
        registered_hackathons = HackathonRegister.objects.filter(user=user).values_list('hackathon', flat=True)
        hackathons = Hackathon.objects.filter(id__in=registered_hackathons).order_by("start_time")
        response = HackathonSerializer(hackathons, many=True).data
        
        return Response(response, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)