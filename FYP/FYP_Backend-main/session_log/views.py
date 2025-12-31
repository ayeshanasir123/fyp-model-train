# ... (Imports)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import session_log
from .serializers import SessionLogSerializer

@api_view(['GET', 'POST'])
def sessionlog_list_create(request):
    if request.method == 'GET':
        items = session_log.objects.all()
        serializer = SessionLogSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SessionLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sessionlog_detail(request, pk):
    item = get_object_or_404(session_log, pk=pk)
    if request.method == 'GET':
        serializer = SessionLogSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SessionLogSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)