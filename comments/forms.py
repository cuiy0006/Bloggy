from django import forms
from .models import Comment, CommentExtension


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentExtensionForm(forms.ModelForm):
    class Meta:
        model = CommentExtension
        fields = []