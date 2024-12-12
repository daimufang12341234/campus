from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    """帖子模型
    用于存储用户发布的帖子信息
    """
    CATEGORY_CHOICES = [
        ('confession', '表白墙'),
        ('life', '校园生活分享'),
        ('sale', '出售墙'),
        ('buy', '求购墙'),
        ('qa', '解答墙'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')  # 帖子作者，关联到Django的用户模型
    title = models.CharField(max_length=200, verbose_name='标题', default='')  # 帖子标题
    content = models.TextField(verbose_name='内容', default='')  # 帖子内容
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='图片')  # 帖子图片，按日期存储
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')  # 创建时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 更新时间，自动更新
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name='点赞')  # 点赞用户，多对多关系
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')  # 添加浏览量字段
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='life',
        verbose_name='分类'
    )

    class Meta:
        ordering = ['-created_at']  # 按创建时间倒序排序
        verbose_name = '帖子'
        verbose_name_plural = '帖子'

    def __str__(self):
        return self.title or f'Post {self.id}'
    
    def like_count(self):
        """获取帖子的点赞数"""
        return self.likes.count()

class Comment(models.Model):
    """评论模型
    用于存储用户对帖子的评论
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')  # 关联的帖子
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')  # 评论作者
    content = models.TextField(verbose_name='评论内容')  # 评论内容
    created_at = models.DateTimeField(default=timezone.now, verbose_name='评论时间')  # 评论时间
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True, verbose_name='点赞')  # 新点赞字段

    class Meta:
        ordering = ['-created_at']  # 按创建时间倒序排序
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.author.username} 评论了 {self.post.title}'
    
    def like_count(self):
        """获取评论的点赞数"""
        return self.likes.count()

class Friendship(models.Model):
    """好友关系模型"""
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立时间')

    class Meta:
        verbose_name = '好友关系'
        verbose_name_plural = '好友关系'
        unique_together = ('user1', 'user2')  # 防止重复的好友关系

    def __str__(self):
        return f'{self.user1.username} - {self.user2.username}'

class UserProfile(models.Model):
    """用户资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birthday = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=20, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    friends = models.ManyToManyField('self', blank=True)
    bookmarks = models.ManyToManyField('Post', related_name='bookmarked_by', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def follow_count(self):
        return self.following.count()

    def follower_count(self):
        return self.followers.count()

# 添加信号接收器，在创建用户时自动创建用户资料
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """当创建新用户时自动创建用户资料"""
    if created:
        try:
            # 检查是否已存在 UserProfile
            UserProfile.objects.get(user=instance)
        except UserProfile.DoesNotExist:
            # 不存在则创建
            UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时同时保存用户资料"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

class Feedback(models.Model):
    """用���反馈模型
    用于存储用户提交的反馈信息
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')  # 提交反馈的用户
    content = models.TextField(verbose_name='反馈内容')  # 反馈内容
    created_at = models.DateTimeField(default=timezone.now, verbose_name='提交时间')  # 提交时间
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待处理'),
            ('processing', '处理中'),
            ('resolved', '已解决'),
            ('closed', '已关闭')
        ],
        default='pending',
        verbose_name='状态'
    )  # 反馈状态
    reply = models.TextField(blank=True, null=True, verbose_name='管理员回复')  # 管理员回复内容
    replied_at = models.DateTimeField(blank=True, null=True, verbose_name='回复时间')  # 回复时间
    replied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replied_feedbacks',
        verbose_name='回复管理员'
    )  # 回复的管理员

    class Meta:
        ordering = ['-created_at']  # 按创建时间倒序排序
        verbose_name = '用户反馈'
        verbose_name_plural = '用户反馈'

    def __str__(self):
        return f'{self.user.username}的反馈 - {self.created_at.strftime("%Y-%m-%d")}'

class FriendRequest(models.Model):
    """好友请求模型"""
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE, verbose_name='发送者')
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE, verbose_name='接收者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待处理'),
            ('accepted', '已接受'),
            ('rejected', '已拒绝')
        ],
        default='pending',
        verbose_name='状态'
    )

    class Meta:
        verbose_name = '好友请求'
        verbose_name_plural = '好友请求'
        unique_together = ('from_user', 'to_user')  # 防止重复发送请求

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'

class Message(models.Model):
    """私信消息模型"""
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, verbose_name='发送者')
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, verbose_name='接收者')
    content = models.TextField(verbose_name='消息内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        ordering = ['created_at']
        verbose_name = '私信'
        verbose_name_plural = '私信'

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

class Notification(models.Model):
    """系统通知模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '系统通知'
        verbose_name_plural = '系统通知'

    def __str__(self):
        return self.title

class DailyStatistics(models.Model):
    """每日统计数据模型"""
    date = models.DateField(unique=True, verbose_name='日期')
    visit_count = models.IntegerField(default=0, verbose_name='访问人数')
    post_count = models.IntegerField(default=0, verbose_name='发帖数量')
    new_user_count = models.IntegerField(default=0, verbose_name='新用户数量')

    class Meta:
        ordering = ['-date']
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'

    def __str__(self):
        return f"{self.date} 统计"
