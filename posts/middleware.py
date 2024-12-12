from django.utils import timezone
from .models import DailyStatistics

class DailyStatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        try:
            # 只统计正常页面访问
            if (request.method == 'GET' and 
                not request.path.startswith('/static/') and 
                not request.path.startswith('/media/') and
                not request.headers.get('X-Requested-With') == 'XMLHttpRequest'):
                
                today = timezone.now().date()
                stats, created = DailyStatistics.objects.get_or_create(date=today)
                stats.visit_count += 1
                stats.save()
        except Exception as e:
            print(f"统计访问量时出错: {e}")
        
        return response 