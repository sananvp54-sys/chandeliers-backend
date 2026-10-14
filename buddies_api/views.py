from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ihrd
from .serializers import IhrdSerializer

@api_view(['GET', 'POST'])
def buddies_list(request):
    if request.method == 'GET':
        buddies = Ihrd.objects.all()
        serializer = IhrdSerializer(buddies, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = IhrdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
