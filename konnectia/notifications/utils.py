from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def create_notification(recipient, sender, notification_type, post=None, comment=None):
    """Create a notification and send it through WebSocket"""
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        post=post,
        comment=comment
    )
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.id}",
        {
            "type": "send_notification",
            "notification": {
                "id": notification.id,
                "type": notification.notification_type,
                "sender": {
                    "username": sender.username,
                    "profile_pic": sender.profile_pic.url if sender.profile_pic else None
                },
                "post_id": post.id if post else None,
                "comment_id": comment.id if comment else None,
                "created_at": notification.created_at.isoformat(),
                "is_read": notification.is_read
            }
        }
    )
    return notification 