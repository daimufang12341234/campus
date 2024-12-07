from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Comment, UserProfile, Feedback, FriendRequest, Friendship, Message
from .forms import PostForm, CommentForm, UserProfileForm, UserRegistrationForm, FeedbackForm, FeedbackReplyForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib import messages
from django.utils import timezone

def post_list(request):
    """帖子列表视图
    显示所有帖子，支持搜索和分页功能
    """
    # 获取搜索关键词
    query = request.GET.get('q', '')
    
    # 基础查询：获取所有帖子
    post_list = Post.objects.all()
    
    # 如果有搜索关键词，过滤结果
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |  # 标题包含关键词
            Q(content__icontains=query) |  # 内容包含关键词
            Q(author__username__icontains=query)  # 作者名包含关键词
        )
    
    # 按创建时间倒序排序
    post_list = post_list.order_by('-created_at')
    
    # 分页处理：每页显示9个帖子
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'posts': posts,
        'page_obj': posts,
        'query': query,  # 将搜索词传递给模板
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create(request):
    """创建帖子视图
    需要用户登录，处理帖子的创建表单
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 设置帖子作者为当前用户
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    """帖子详情视图
    显示帖子详情，处理评论提交
    """
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def like_post(request, post_id):
    """帖子点赞视图
    处理帖子的点赞和取消点赞
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # 取消点赞
            liked = False
        else:
            post.likes.add(request.user)  # 添加点赞
            liked = True
        return JsonResponse({
            'liked': liked,
            'count': post.like_count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def user_profile(request, username):
    """用户个人主页视图"""
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).order_by('-created_at')
    
    # 获取好友状态和请求状态
    is_friend = False
    friend_request = None
    if request.user.is_authenticated and request.user != user:
        is_friend = request.user.userprofile.friends.filter(id=user.id).exists()
        if not is_friend:
            friend_request = FriendRequest.objects.filter(
                from_user=request.user,
                to_user=user,
                status='pending'
            ).first()
    
    # 分页处理
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'profile_user': user,
        'posts': posts,
        'page_obj': posts,
        'is_owner': request.user == user,
        'total_posts': post_list.count(),
        'total_likes': sum(post.like_count() for post in post_list),
        'friend_request': friend_request,
        'is_friend': is_friend,  # 添加好友状态到上下文
    }
    return render(request, 'posts/user_profile.html', context)

@login_required
def edit_profile(request):
    """编辑个人资料视图
    处理用户资料的更新
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('posts:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'posts/edit_profile.html', {'form': form})

@login_required
def follow_user(request, username):
    """关注用户视图
    处理用户关注和取消关注
    """
    user_to_follow = get_object_or_404(User, username=username)
    profile = request.user.userprofile
    
    if request.user != user_to_follow:
        if user_to_follow.userprofile in profile.following.all():
            profile.following.remove(user_to_follow.userprofile)  # 取消关注
            is_following = False
        else:
            profile.following.add(user_to_follow.userprofile)  # 添加关注
            is_following = True
        
        return JsonResponse({
            'is_following': is_following,
            'follower_count': user_to_follow.userprofile.follower_count()
        })
    return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = request.user.userprofile
    
    if post in profile.bookmarks.all():
        profile.bookmarks.remove(post)
        bookmarked = False
    else:
        profile.bookmarks.add(post)
        bookmarked = True
    
    return JsonResponse({
        'bookmarked': bookmarked
    })

@login_required
def bookmarked_posts(request):
    bookmarks = request.user.userprofile.bookmarks.all()
    return render(request, 'posts/bookmarked_posts.html', {'posts': bookmarks})

# 添加退出登录视图
def user_logout(request):
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('posts:post_list')

# 添加删除帖子视图
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # 检查是否是作者或超级用户
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, '帖子已成功删除')
        return redirect('posts:post_list')
    else:
        messages.error(request, '您没有权限删除这个帖子')
        return redirect('posts:post_detail', post_id=post_id)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # 创建用户但不保存到数据库
            user = form.save(commit=False)
            # 保存用户
            user.save()
            # 登录新用户
            login(request, user)
            messages.success(request, '注册成功！欢迎加入校园生活分享。')
            return redirect('posts:post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'posts/register.html', {'form': form})

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, '感谢您的反馈！我们会尽快处理。')
            return redirect('posts:my_feedbacks')
    else:
        form = FeedbackForm()
    return render(request, 'posts/submit_feedback.html', {'form': form})

@login_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'posts/my_feedbacks.html', {'feedbacks': feedbacks})

@login_required
def manage_feedbacks(request):
    if not request.user.is_superuser:
        messages.error(request, '您没有权限访问此页面')
        return redirect('posts:post_list')
    
    feedbacks = Feedback.objects.all()
    return render(request, 'posts/manage_feedbacks.html', {'feedbacks': feedbacks})

@login_required
def reply_feedback(request, feedback_id):
    if not request.user.is_superuser:
        messages.error(request, '您没有权限执行此操作')
        return redirect('posts:post_list')
    
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        form = FeedbackReplyForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.replied_by = request.user
            feedback.replied_at = timezone.now()
            feedback.save()
            messages.success(request, '回复已发送')
            return redirect('posts:manage_feedbacks')
    else:
        form = FeedbackReplyForm(instance=feedback)
    
    return render(request, 'posts/reply_feedback.html', {
        'form': form,
        'feedback': feedback
    })

@login_required
def manage_users(request):
    """用户管理视图
    仅超级用户可访问，用于管理所有普通用户
    """
    if not request.user.is_superuser:
        messages.error(request, '您没有权限访问此页面')
        return redirect('posts:post_list')
    
    # 获取所有普通用户（非超级用户）
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    # 分页处理
    paginator = Paginator(users, 20)  # 每页显示20个用户
    page = request.GET.get('page')
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    return render(request, 'posts/manage_users.html', {
        'users': users,
        'page_obj': users,
    })

@login_required
def toggle_user_active(request, user_id):
    """切换用户状态（启用/禁用）
    仅超级用户可操作
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': '权限不足'}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return JsonResponse({'error': '不能修改超级用户状态'}, status=400)
        
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'is_active': user.is_active,
            'message': f'用户 {user.username} 已{"启用" if user.is_active else "禁用"}'
        })
    except User.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)

@login_required
def like_comment(request, comment_id):
    """评论点赞视图
    ���理评论的点赞和取消点赞
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)  # 取消点赞
            liked = False
        else:
            comment.likes.add(request.user)  # 添加点赞
            liked = True
        return JsonResponse({
            'liked': liked,
            'count': comment.like_count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_comment(request, comment_id):
    """删除评论视图
    仅评论作者和超级用户可以删除评论
    """
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    
    # 检查是否是评论作者或超级用户
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        messages.success(request, '评论已成功删除')
    else:
        messages.error(request, '您没有权限删除这条评论')
    
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def send_friend_request(request, username):
    """发送好友请求"""
    to_user = get_object_or_404(User, username=username)
    
    # 检查是否是自己
    if request.user == to_user:
        messages.error(request, '不能添加自己为好友')
        return redirect('posts:user_profile', username=username)
    
    # 检查是否已经是好友
    if request.user.userprofile.friends.filter(id=to_user.id).exists():
        messages.info(request, '已经是好友了')
        return redirect('posts:user_profile', username=username)
    
    # 检查是否有待处理的请求（从我发送给对方的）
    existing_request = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).first()
    
    if existing_request:
        if existing_request.status == 'pending':
            messages.info(request, '已经发送过好友请求了')
        elif existing_request.status == 'accepted':
            messages.info(request, '你们已经是好友了')
        elif existing_request.status == 'rejected':
            # 如果之前的请求被拒绝，允许重新发送
            existing_request.status = 'pending'
            existing_request.created_at = timezone.now()
            existing_request.save()
            messages.success(request, f'已向 {to_user.username} 重新发送好友请求')
        return redirect('posts:user_profile', username=username)
    
    # 检查是否有待处理的请求（从对方发送给我的）
    reverse_request = FriendRequest.objects.filter(
        from_user=to_user,
        to_user=request.user
    ).first()
    
    if reverse_request:
        if reverse_request.status == 'pending':
            messages.info(request, f'{to_user.username} 已经向你发送了好友请求，请查看你的好友请求列表')
        elif reverse_request.status == 'accepted':
            messages.info(request, '你们已经是好友了')
        elif reverse_request.status == 'rejected':
            # 如果对方的请求被拒绝，允许发送新请求
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            messages.success(request, f'已向 {to_user.username} 发送好友请求')
        return redirect('posts:user_profile', username=username)
    
    # 如果没有任何已存在的请求，创建新请求
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    messages.success(request, f'已向 {to_user.username} 发送好友请求')
    return redirect('posts:user_profile', username=username)

@login_required
def friend_requests(request):
    """查看好友请求列表"""
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    return render(request, 'posts/friend_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def handle_friend_request(request, request_id, action):
    """处理好友请求"""
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        
        # 创建双向好友关系
        request.user.userprofile.friends.add(friend_request.from_user)
        friend_request.from_user.userprofile.friends.add(request.user)
        
        messages.success(request, f'已接受 {friend_request.from_user.username} 的好友请求')
    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        messages.success(request, f'已拒绝 {friend_request.from_user.username} 的好友请求')
    
    return redirect('posts:friend_requests')

@login_required
def friend_list(request):
    """查看好友列表"""
    # 获取当前用户的好友列表（直接获取User对象）
    friends = User.objects.filter(id__in=request.user.userprofile.friends.all())
    return render(request, 'posts/friend_list.html', {'friends': friends})

@login_required
def chat(request, username):
    """私信聊天"""
    friend = get_object_or_404(User, username=username)
    
    # 检查是否是好友关系
    if not request.user.userprofile.friends.filter(id=friend.id).exists():
        messages.error(request, '只能与好友聊天')
        return redirect('posts:user_profile', username=username)
    
    # 获取聊天记录
    chat_messages = Message.objects.filter(
        (Q(sender=request.user, receiver=friend) | Q(sender=friend, receiver=request.user))
    ).order_by('created_at')
    
    # 标记消息为已读
    Message.objects.filter(sender=friend, receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=friend, content=content)
            return redirect('posts:chat', username=username)
    
    return render(request, 'posts/chat.html', {
        'friend': friend,
        'messages': chat_messages
    })

@login_required
def chat_list(request):
    """聊天列表"""
    # 获取所有聊天过的好友
    chat_friends = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    
    # 获取每个好友的最后一条消息和未读消息数
    chats = []
    for friend in chat_friends:
        last_message = Message.objects.filter(
            (Q(sender=request.user, receiver=friend) | Q(sender=friend, receiver=request.user))
        ).order_by('-created_at').first()
        
        unread_count = Message.objects.filter(
            sender=friend, receiver=request.user, is_read=False
        ).count()
        
        chats.append({
            'friend': friend,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    return render(request, 'posts/chat_list.html', {'chats': chats})

@login_required
def remove_friend(request, username):
    """删除好友视图"""
    friend = get_object_or_404(User, username=username)
    
    # 检查是否是好友关系
    if not request.user.userprofile.friends.filter(id=friend.id).exists():
        messages.error(request, '该用户不是您的好友')
        return redirect('posts:user_profile', username=username)
    
    # 删除好友关系（双向）
    Friendship.objects.filter(
        (Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user))
    ).delete()
    
    # 从好友列表中移除
    request.user.userprofile.friends.remove(friend.userprofile)
    
    messages.success(request, f'已将 {friend.username} 从好友列表中移除')
    return redirect('posts:friend_list')

def welcome(request):
    """欢迎页面视图"""
    return render(request, 'posts/welcome.html')
