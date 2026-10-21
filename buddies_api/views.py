from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ihrd
from .serializers import IhrdSerializer

@api_view(['GET', 'POST'])
def buddies_list(request):
    if request.method == 'GET':
        return Response(IhrdSerializer(Ihrd.objects.all(), many=True).data)

    if not settings.DEBUG:
        return Response({'detail': 'Add members from the admin panel.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = IhrdSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)