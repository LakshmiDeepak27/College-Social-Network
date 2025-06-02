from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:20]
    return JsonResponse({
        'notifications': [{
            'id': notification.id,
            'type': notification.notification_type,
            'sender': {
                'username': notification.sender.username,
                'profile_pic': notification.sender.profile_pic.url if notification.sender.profile_pic else None
            },
            'post_id': notification.post.id if notification.post else None,
            'comment_id': notification.comment.id if notification.comment else None,
            'created_at': notification.created_at.isoformat(),
            'is_read': notification.is_read
        } for notification in notifications]
    })

@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404) 