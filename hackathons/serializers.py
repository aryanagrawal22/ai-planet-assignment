from rest_framework import serializers
from hackathons.models import Hackathon

class HackathonSerializer(serializers.ModelSerializer):

    class Meta:

        model = Hackathon
        fields = ['id','title', 'description','background_image','hackathon_image','start_time','end_time','reward_prize']