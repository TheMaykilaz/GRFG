from django import forms
from .models import ForumComment

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш коментар...'}),
        }
