from rest_framework import serializers
from submissions.models import Submission
from hackathons.serializers import HackathonSerializer
from users.serializers import UserSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    hackathon = serializers.SerializerMethodField(source='get_hackathon')
    user = serializers.SerializerMethodField(source='get_user')
    class Meta:

        model = Submission
        fields = ['id','title', 'summary','created_at','user','hackathon']
        
    def get_hackathon(self, obj):
        return HackathonSerializer(obj.hackathon, many=False).data
    
    def get_user(self, obj):
        return UserSerializer(obj.user, many=False).data
        