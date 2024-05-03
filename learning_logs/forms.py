from django import forms

from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"] # Try to set something different later
        labels = {"text": ""}
        