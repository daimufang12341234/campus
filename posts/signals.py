from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post, DailyStatistics

@receiver(post_save, sender=Post)
def update_post_count(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        stats, _ = DailyStatistics.objects.get_or_create(date=today)
        stats.post_count += 1
        stats.save()

@receiver(post_save, sender=User)
def update_user_count(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        stats, _ = DailyStatistics.objects.get_or_create(date=today)
        stats.new_user_count += 1
        stats.save() 