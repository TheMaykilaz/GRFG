from django import forms
from .models import ForumComment
from .models import ForumTopic

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть коментар...'}),
        }

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title']