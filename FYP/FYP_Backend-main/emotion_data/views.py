from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# --- ADD THIS IMPORT ---
# This allows 'emotion_data.objects' to be recognized
from .models import emotion_data 
from .serializers import EmotionDataSerializer

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def emotion_list_create(request):
    if request.method == 'GET':
        client_id = request.query_params.get('client_id')
        
        # Now 'emotion_data' is recognized
        if client_id:
            emotions = emotion_data.objects.filter(client_id=client_id).order_by('-emotion_id')
        else:
            emotions = emotion_data.objects.all().order_by('-emotion_id')
            
        serializer = EmotionDataSerializer(emotions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("Incoming Emotion Data:", request.data)
        
        serializer = EmotionDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Serializer Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)