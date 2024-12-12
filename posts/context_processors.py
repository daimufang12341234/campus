from .models import Message, FriendRequest, Feedback, Post, Notification
import json
from django.utils.html import escapejs

def notifications(request):
    if request.user.is_authenticated:
        try:
            active_notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
            
            # 序列化通知数据
            notifications_data = [
                {
                    'id': notification.id,
                    'title': str(notification.title),
                    'content': str(notification.content)
                }
                for notification in active_notifications
            ]
            
            context = {
                'unread_messages_count': Message.objects.filter(
                    receiver=request.user,
                    is_read=False
                ).count(),
                'friend_requests_count': FriendRequest.objects.filter(
                    to_user=request.user,
                    status='pending'
                ).count(),
                'notifications': active_notifications,
                'notifications_json': json.dumps(notifications_data)
            }
            
            if request.user.is_superuser:
                context['pending_feedbacks_count'] = Feedback.objects.filter(
                    status='pending'
                ).count()
                
            return context
        except Exception as e:
            print(f"通知处理错误: {str(e)}")
            return {}
    return {} 

def post_categories(request):
    return {
        'post_categories': Post.CATEGORY_CHOICES
    } 