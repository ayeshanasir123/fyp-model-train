# ... (Imports)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import session_log
from .serializers import SessionLogSerializer
import google.generativeai as genai
from ai_guidance.models import ai_guidance
from emotion_data.models import emotion_data
from django.db.models import Avg

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def sessionlog_list_create(request):
    if request.method == 'GET':
        # Filter by client_id if provided
        client_id = request.query_params.get('client_id')
        if client_id:
            items = session_log.objects.filter(client_id=client_id)
        else:
            items = session_log.objects.all()
        serializer = SessionLogSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            # Auto-generate date and handle coach_id
            from datetime import date
            from client.models import client
            
            data = request.data.copy()
            client_id = data.get('client_id')
            
            print(f"[Session Creation] Received request with client_id: {client_id}")
            print(f"[Session Creation] Full data: {data}")
            
            # Validate that client exists
            if not client_id:
                return Response({"error": "client_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                client_obj = client.objects.get(client_id=client_id)
                print(f"[Session Creation] Found client: {client_obj}")
            except client.DoesNotExist:
                return Response({
                    "error": f"Client with ID {client_id} does not exist. Please ensure you have a client profile."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data['date'] = date.today()
            data['notes'] = data.get('notes', '')
            
            # Map coach_id to user_id if provided, otherwise set to None
            if 'coach_id' in data:
                data['user_id'] = data.pop('coach_id')
            if 'user_id' not in data or data['user_id'] is None:
                data['user_id'] = None
            
            print(f"[Session Creation] Prepared data: {data}")
            
            serializer = SessionLogSerializer(data=data)
            if serializer.is_valid():
                session = serializer.save()
                print(f"[Session Created] ID: {session.session_id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"[Session Error] Validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"[Session Error] Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_session_summary(request, session_id):
    """
    Generate AI summary of the conversation and detect final emotion
    Called when user ends a chat session
    """
    try:
        # Get the session
        session = get_object_or_404(session_log, session_id=session_id)
        
        # Get all conversation messages for this session
        conversations = ai_guidance.objects.filter(
            session_id_id=session_id
        ).order_by('created_at')
        
        if not conversations.exists():
            return Response({
                "error": "No conversation found for this session"
            }, status=400)
        
        # Build conversation history for summarization
        conversation_text = ""
        for conv in conversations:
            conversation_text += f"User: {conv.user_message}\n"
            conversation_text += f"AI: {conv.ai_response}\n\n"
        
        # Get final emotion from the last emotion recorded in this session
        final_emotion_record = emotion_data.objects.filter(
            session_id_id=session_id
        ).order_by('-created_at').first()
        
        # Calculate average emotion intensity for the session
        avg_intensity = emotion_data.objects.filter(
            session_id_id=session_id
        ).aggregate(Avg('intensity'))['intensity__avg'] or 0
        
        # Generate summary using Gemini
        genai.configure(api_key="AIzaSyBp1bNtBS5bUg8mc45m6bU_J3e0REtfzhA", transport='rest')
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        summary_prompt = f"""
        You are a professional mental health therapist. Analyze this conversation and provide a concise, professional summary.
        
        Conversation:
        {conversation_text}
        
        Please provide:
        1. A brief summary of the main topics discussed (2-3 sentences)
        2. Key concerns or issues identified
        3. Progress or insights gained
        4. Recommended follow-up actions
        
        Keep the summary professional, empathetic, and actionable. Format it in clear paragraphs.
        """
        
        response = model.generate_content(summary_prompt)
        summary = response.text
        
        # Update session with summary and final emotion
        session.summary = summary
        session.final_emotion = final_emotion_record.emotion if final_emotion_record else "neutral"
        session.emotion_intensity = int(avg_intensity)
        session.save()
        
        return Response({
            "session_id": session_id,
            "summary": summary,
            "final_emotion": session.final_emotion,
            "emotion_intensity": session.emotion_intensity,
            "message_count": conversations.count(),
            "session_date": session.date
        })
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)