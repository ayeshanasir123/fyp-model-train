"""
Dataset Export Service
Exports stored conversations for training emotion detection models
"""

import csv
import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from ai_guidance.models import ai_guidance
from emotion_data.models import emotion_data


def export_conversations_as_tsv(request):
    """
    Export all conversations in TSV format compatible with GoEmotions dataset
    Format: text\temotions\tid
    """
    # Get all conversations with emotions
    conversations = ai_guidance.objects.select_related('emotion_id').all()
    
    # Create HTTP response with TSV format
    response = HttpResponse(content_type='text/tab-separated-values')
    response['Content-Disposition'] = f'attachment; filename="conversation_dataset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tsv"'
    
    writer = csv.writer(response, delimiter='\t')
    
    # Write data
    for conv in conversations:
        text = conv.user_message if conv.user_message else ""
        emotion = conv.emotion_id.emotion if conv.emotion_id else "neutral"
        conv_id = f"conv_{conv.guidance_id}"
        
        # Clean text (remove newlines, tabs)
        text = text.replace('\n', ' ').replace('\t', ' ').strip()
        
        writer.writerow([text, emotion, conv_id])
    
    return response


def export_conversations_as_json(request):
    """
    Export all conversations in JSON format with complete data
    """
    conversations = ai_guidance.objects.select_related('emotion_id', 'client_id', 'session_id').all()
    
    dataset = []
    for conv in conversations:
        dataset.append({
            'guidance_id': conv.guidance_id,
            'user_message': conv.user_message,
            'ai_response': conv.ai_response,
            'emotion': conv.emotion_id.emotion if conv.emotion_id else 'neutral',
            'intensity': conv.emotion_id.intensity if conv.emotion_id else 5,
            'client_id': conv.client_id.client_id if conv.client_id else None,
            'session_id': conv.session_id.session_id if conv.session_id else None,
            'created_at': conv.created_at.isoformat(),
            'effectiveness': conv.effectiveness
        })
    
    response = HttpResponse(json.dumps(dataset, indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="conversation_dataset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
    
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_stats(request):
    """
    Get statistics about the conversation dataset
    """
    total_conversations = ai_guidance.objects.count()
    
    # Emotion distribution
    emotion_distribution = (
        emotion_data.objects
        .values('emotion')
        .annotate(count=Count('emotion_id'))
        .order_by('-count')
    )
    
    # Conversations per client
    client_stats = (
        ai_guidance.objects
        .values('client_id')
        .annotate(conv_count=Count('guidance_id'))
    )
    
    # Conversations per session
    session_stats = (
        ai_guidance.objects
        .values('session_id')
        .annotate(conv_count=Count('guidance_id'))
    )
    
    # Date range
    first_conversation = ai_guidance.objects.order_by('created_at').first()
    last_conversation = ai_guidance.objects.order_by('-created_at').first()
    
    stats = {
        'total_conversations': total_conversations,
        'total_emotions_recorded': emotion_data.objects.count(),
        'unique_clients': client_stats.count(),
        'unique_sessions': session_stats.count(),
        'emotion_distribution': list(emotion_distribution),
        'date_range': {
            'first': first_conversation.created_at.isoformat() if first_conversation else None,
            'last': last_conversation.created_at.isoformat() if last_conversation else None
        },
        'avg_conversations_per_client': sum(s['conv_count'] for s in client_stats) / max(client_stats.count(), 1),
        'ready_for_training': total_conversations >= 100  # Minimum for basic training
    }
    
    return JsonResponse(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def export_for_training(request):
    """
    Main endpoint to export data for model training
    Supports multiple formats via query parameter
    """
    export_format = request.GET.get('format', 'tsv')
    
    if export_format == 'json':
        return export_conversations_as_json(request)
    else:  # Default to TSV
        return export_conversations_as_tsv(request)
