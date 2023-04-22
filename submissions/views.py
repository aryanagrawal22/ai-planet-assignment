from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from hackathons.models import Hackathon, HackathonRegister
from utility.authMiddleware import is_authenticated
import datetime
from django.db.models import Q
from hackathons.serializers import HackathonSerializer
from pytz import UTC
from submissions.models import Submission
from submissions.serializers import SubmissionSerializer

@api_view(['GET'])
@is_authenticated
def create_submission(request):
    try:
        user = request.user
        title = request.data.get('title')
        summary = request.data.get('summary')
        hackathon_id = request.data.get('hackathon_id')
        
        if hackathon_id is None:
            return Response({'error': "hackathon_id is needed to register"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Hackathon.objects.filter(id=hackathon_id).exists():
            return Response({'error': "Hackathon does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        
        if hackathon.end_time<datetime.datetime.now().replace(tzinfo=UTC):
            return Response({'error': "Hackathon has ended"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not HackathonRegister.objects.filter(Q(Q(user=user)&Q(hackathon=hackathon))).exists():
            return Response({'error': "User not registered to hackathon"}, status=status.HTTP_400_BAD_REQUEST)
        
        Submission.objects.create(
                    title=title,
                    summary=summary,
                    hackathon=hackathon,
                    user=user,
                )
        return Response("Submission Created", status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET'])
@is_authenticated
def get_submissions(request):
    try:
        user = request.user
        
        registered_hackathons = HackathonRegister.objects.filter(user=user).values_list('hackathon', flat=True)
        submissions = Submission.objects.filter(Q(Q(hackathon__in=registered_hackathons)&Q(user=user))).order_by("-created_at")
        response = SubmissionSerializer(submissions, many=True).data
        return Response(response, status=status.HTTP_200_OK)
    
    except Exception as exception:
        return Response({'error': str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)