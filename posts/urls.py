from django.urls import path
from . import views

app_name = 'posts'  # 应用命名空间，用于URL反向解析

urlpatterns = [
    path('', views.welcome, name='welcome'),  # 欢迎页面
    path('home/', views.post_list, name='post_list'),  # 帖子列表页（首页）
    path('create/', views.post_create, name='post_create'),  # 创建新帖子
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # 帖子详情页
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),  # 帖子点赞功能
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # 删除帖子
    
    # 用户相关的URL
    path('user/<str:username>/', views.user_profile, name='user_profile'),  # 用户个人主页
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # 编辑个人资料
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),  # 关注用户
    path('register/', views.register, name='register'),  # 用户注册
    path('logout/', views.user_logout, name='logout'),  # 退出登录
    
    # 收藏功能相关的URL
    path('post/<int:post_id>/bookmark/', views.bookmark_post, name='bookmark_post'),  # 收藏帖子
    path('bookmarks/', views.bookmarked_posts, name='bookmarked_posts'),  # 查看收藏的帖子
    
    # 反馈功能相关的URL
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),  # 提交反馈
    path('feedback/my/', views.my_feedbacks, name='my_feedbacks'),  # 查看我的反馈
    path('feedback/manage/', views.manage_feedbacks, name='manage_feedbacks'),  # 管理反馈（管理员）
    path('feedback/<int:feedback_id>/reply/', views.reply_feedback, name='reply_feedback'),  # 回复反馈
    path('users/manage/', views.manage_users, name='manage_users'),
    path('users/<int:user_id>/toggle-active/', views.toggle_user_active, name='toggle_user_active'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('friend-request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('friend-request/<int:request_id>/<str:action>/', views.handle_friend_request, name='handle_friend_request'),
    path('friends/', views.friend_list, name='friend_list'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('friend/<str:username>/remove/', views.remove_friend, name='remove_friend'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/notification/create/', views.create_notification, name='create_notification'),
    path('notification/<int:notification_id>/toggle/', views.toggle_notification, name='toggle_notification'),
] 