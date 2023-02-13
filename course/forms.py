from django import forms
from tinymce import TinyMCE
from .models import Post


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    title = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write a title to a post",
            "class": "input-field",
        }))

    overview = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write an overview to a post",
            "class": "input-field",
        }))

    class Meta:
        model = Post
        fields = ['title', 'overview', 'content', 'thumbnail']
