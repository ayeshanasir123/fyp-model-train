import google.generativeai as genai
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ai_guidance
from .serializers import AIGuidanceSerializer
from .goemotions_bert_detector import get_emotion_detector
from emotion_data.models import emotion_data

# --- Configure Gemini ---
# Keep transport='rest' to help with the connection issues we saw earlier
genai.configure(api_key="AIzaSyBF4TbLwpbR0jajrRZQgyDHNDS2ldR6rFM", transport='rest')

THERAPIST_PROMPT = (
    "You are an empathetic, professional AI Mental Health Guide. "
    "Use CBT techniques and active listening. Always prioritize safety. "
    "If the user is in crisis, provide emergency hotline info. "
    "Keep responses warm, supportive, and reflective."
)

# Update your model initialization to include system_instruction
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-lite',
    system_instruction=THERAPIST_PROMPT  # <--- This is the magic line
)   

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def aiguidance_list_create(request):
    if request.method == 'GET':
        # Return history
        client_id = request.query_params.get('client_id')
        
        if client_id:
            # 2. Only fetch messages belonging to this user
            guidances = ai_guidance.objects.filter(client_id_id=client_id).order_by('created_at')
        else:
            # Fallback if no ID is provided (optional: return empty list)
            guidances = ai_guidance.objects.none()
            
        serializer = AIGuidanceSerializer(guidances, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        try:
            user_message = request.data.get('user_message')
            client_id = request.data.get('client_id')
            session_id = request.data.get('session_id')
            
            print(f"[DEBUG] User message: {user_message}")
            
            if not user_message:
                return Response({"error": "No message provided"}, status=400)
            
            # === EMOTION DETECTION ===
            emotion_detector = get_emotion_detector()
            emotion_result = emotion_detector.detect_emotion(user_message)
            
            print(f"[EMOTION] Detected: {emotion_result['emotion']} (confidence: {emotion_result['confidence']}, intensity: {emotion_result['intensity']})")
            
            # Save emotion to emotion_data table
            emotion_record = emotion_data.objects.create(
                client_id_id=client_id,
                session_id_id=session_id,
                emotion=emotion_result['emotion'],
                intensity=emotion_result['intensity'],
                notes=f"Detected from message with {emotion_result['confidence']*100:.1f}% confidence"
            )
            
            # === ENHANCED AI PROMPT ===
            # Add emotion context to the prompt for better AI response
            enhanced_message = emotion_detector.enhance_prompt_with_emotion(
                user_message, 
                emotion_result
            )
            
            print(f"[AI] Sending enhanced prompt with emotion context")
            
            # Generate AI response with emotion-aware context
            response = model.generate_content(enhanced_message)
            ai_response = response.text
            
            print(f"[AI] Response generated")

            # Save to database with detected emotion
            guidance_obj = ai_guidance.objects.create(
                client_id_id=client_id,
                session_id_id=session_id, 
                emotion_id=emotion_record,  # Link to the emotion we just created
                user_message=user_message,
                ai_response=ai_response,
                suggestion=f"Emotion-aware response using {emotion_result['approach']} approach"
            )
            
            print(f"[DB] Saved guidance #{guidance_obj.guidance_id}")
            
            # Return response with emotion data
            return Response({
                "response": ai_response,
                "emotion_detected": {
                    "emotion": emotion_result['emotion'],
                    "confidence": emotion_result['confidence'],
                    "intensity": emotion_result['intensity'],
                    "approach": emotion_result['approach'],
                    "tone": emotion_result['tone']
                },
                "guidance_id": guidance_obj.guidance_id
            })

        except Exception as e:
            print(f"--- ERROR --- \n{e}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def aiguidance_detail(request, pk):
    item = get_object_or_404(ai_guidance, pk=pk)
    
    if request.method == 'GET':
        serializer = AIGuidanceSerializer(item)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = AIGuidanceSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)