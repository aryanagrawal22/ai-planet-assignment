from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

@api_view(["GET"])
def default(request):
    return Response("Welcome to AI-Planet-Assignment")