from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'is_draft']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # ✅ 'text' exists on Comment model
