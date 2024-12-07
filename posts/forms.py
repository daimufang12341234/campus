from django import forms
from .models import Post, Comment, UserProfile, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    """帖子表单
    用于创建和编辑帖子的表单类
    """
    class Meta:
        model = Post  # 关联到Post模型
        fields = ['title', 'content', 'image']  # 可编辑的字段
        widgets = {
            # 为每个字段添加Bootstrap样式
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    """评论表单
    用于创建评论的表单类
    """
    class Meta:
        model = Comment
        fields = ['content']  # 只需要内容字段
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': '写下你的评论...'
            }),
        }

class UserProfileForm(forms.ModelForm):
    """用户资料表单
    用于编辑用户个人资料的表单类
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']  # 可编辑的个人资料字段
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': '写一些关于你自己的介绍...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    """用户注册表单
    扩展Django的用户创建表单，添加额外的字段和验证
    """
    # 添加邮箱字段
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为所有字段添加Bootstrap样式
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_username(self):
        """验证用户名是否已存在"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被使用，请选择其他用户名。')
        return username

    def clean_email(self):
        """验证邮箱是否已被注册"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，请使用其他邮箱。')
        return email

class FeedbackForm(forms.ModelForm):
    """用户反馈表单
    用于提交用户反馈的表单类
    """
    class Meta:
        model = Feedback
        fields = ['content']  # 只需要内容字段
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': '请描述您的建议或遇到的问题...'
            }),
        }

class FeedbackReplyForm(forms.ModelForm):
    """反馈回复表单
    用于管理员回复用户反馈的表单类
    """
    class Meta:
        model = Feedback
        fields = ['reply', 'status']  # 回复内容和状态字段
        widgets = {
            'reply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': '请输入回复内容...'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }