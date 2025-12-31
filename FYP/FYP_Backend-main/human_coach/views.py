# ... (Imports)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import human_coach
from .serializers import HumanCoachSerializer

@api_view(['GET', 'POST'])
def humancoach_list_create(request):
    if request.method == 'GET':
        # ... (list logic with HumanCoachSerializer)
        coaches = human_coach.objects.all()
        serializer = HumanCoachSerializer(coaches, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # ... (create logic with HumanCoachSerializer)
        serializer = HumanCoachSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def humancoach_detail(request, pk):
    coach = get_object_or_404(human_coach, pk=pk)
    # ... (detail/update/delete logic using HumanCoachSerializer)
    if request.method == 'GET':
        serializer = HumanCoachSerializer(coach)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = HumanCoachSerializer(coach, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        coach.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)