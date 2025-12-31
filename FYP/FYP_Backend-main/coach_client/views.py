from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import coach_client
from .serializers import CoachClientSerializer

@api_view(['GET', 'POST'])
def coachclient_list_create(request):
    if request.method == 'GET':
        items = coach_client.objects.all()
        serializer = CoachClientSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CoachClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def coachclient_detail(request, pk):
    item = get_object_or_404(coach_client, pk=pk)
    if request.method == 'GET':
        serializer = CoachClientSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CoachClientSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)