from django.contrib import admin
from .models import Post, Comment, UserProfile, Feedback
from django.utils import timezone

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """帖子管理配置
    配置帖子在管理后台的显示和管理方式
    """
    # 列表页显示的字段
    list_display = ['title', 'author', 'created_at', 'updated_at', 'like_count']
    
    # 列表页可以点击进入编辑页面的字段
    list_display_links = ['title']
    
    # 列表页可以直接编辑的字段
    list_editable = []
    
    # 列表页的过滤器
    list_filter = ['created_at', 'author']
    
    # 搜索字段
    search_fields = ['title', 'content', 'author__username']
    
    # 按日期筛选
    date_hierarchy = 'created_at'
    
    # 只读字段（不可编辑）
    readonly_fields = ['created_at', 'updated_at']
    
    # 自定义方法显示点赞数
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = '点赞数'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """评论管理配置
    配置评论在管理后台的显示和管理方式
    """
    list_display = ['post', 'author', 'content', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理配置
    配置用户资料在管理后台的显示和管理方式
    """
    list_display = ['user', 'follow_count', 'follower_count']
    search_fields = ['user__username', 'bio']
    
    # 自定义方法显示关注数和粉丝数
    def follow_count(self, obj):
        return obj.following.count()
    follow_count.short_description = '关注数'
    
    def follower_count(self, obj):
        return obj.followers.count()
    follower_count.short_description = '粉丝数'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """用户反馈管理配置
    配置用户反馈在管理后台的显示和管理方式
    """
    list_display = ['user', 'content', 'status', 'created_at', 'replied_at', 'replied_by']
    list_filter = ['status', 'created_at', 'replied_at']
    search_fields = ['user__username', 'content', 'reply']
    date_hierarchy = 'created_at'
    
    # 可以直接在列表页修改状态
    list_editable = ['status']
    
    # 只读字段
    readonly_fields = ['created_at', 'replied_at']
    
    # 字段集合，用于组织编辑页面的字段布局
    fieldsets = (
        ('反馈信息', {
            'fields': ('user', 'content', 'created_at')
        }),
        ('处理情况', {
            'fields': ('status', 'reply', 'replied_by', 'replied_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        重写保存方法，自动记录回复人和回复时间
        """
        if 'reply' in form.changed_data:
            obj.replied_by = request.user
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)
