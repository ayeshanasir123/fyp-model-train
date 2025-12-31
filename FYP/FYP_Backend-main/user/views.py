from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Using 'UserModel' as an alias to avoid conflict with the local 'user' variable
from .models import user as UserModel 
from .serializers import UserSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) # Allows React to Signup without a Token
def user_list_create(request):
    """
    List all users or create a new user.
    """
    if request.method == 'GET':
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If data is invalid (e.g. missing email), return the specific errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny]) # Also set to AllowAny for testing; change to IsAuthenticated later
def user_detail(request, pk):
    """
    Retrieve, update or delete a specific user.
    """
    # Renamed variable to 'user_instance' to avoid hiding the UserModel
    user_instance = get_object_or_404(UserModel, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)