from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder": "What's happening?","class": "form-control"}))
    class Meta:
        model = Tweet
        fields = ['content']
