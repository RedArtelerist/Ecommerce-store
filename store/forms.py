from django import forms
from store.models import Comment, Review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['parent', 'name', 'email', 'body']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'body', 'advantages', 'disadvantages', 'rate']