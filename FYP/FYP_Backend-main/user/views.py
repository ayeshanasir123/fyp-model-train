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

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Login user with email and password validation.
    Returns user data along with their client_id if they have a client profile.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = UserModel.objects.get(email=email)
        
        # Check password
        if user.password == password:  # In production, use hashed passwords
            serializer = UserSerializer(user)
            user_data = serializer.data
            
            # Check if this user has a client profile
            from client.models import client
            try:
                # Look for client by user_id, not client_id
                client_profile = client.objects.get(user_id=user.user_id)
                user_data['id'] = client_profile.client_id  # Add client_id as 'id' for frontend
                user_data['client_id'] = client_profile.client_id
                user_data['client_name'] = client_profile.name
                print(f"[Login] User {user.user_id} ({user.email}) logged in with client_id: {client_profile.client_id}")
            except client.DoesNotExist:
                print(f"[Login] User {user.user_id} ({user.email}) has no client profile")
                # For coaches or admin users without client profiles
                user_data['id'] = user.user_id
                user_data['client_id'] = None
            
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except UserModel.DoesNotExist:
        return Response(
            {"error": "User not found. Please sign up first."},
            status=status.HTTP_404_NOT_FOUND
        )

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