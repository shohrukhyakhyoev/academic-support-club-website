from django import forms
from tinymce import TinyMCE
from community.models import Question, QuestionComment, AnswerComment, Answer


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class QuestionForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    title = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "input-field",
        }))

    class Meta:
        model = Question
        fields = ('title', 'content', 'tag', )


class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 50}
        ), label='')

    class Meta:
        model = Answer
        fields = ('content',)


class QuestionCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "comment-textarea",
            "id": "comment"
        }), label='')

    class Meta:
        model = QuestionComment
        exclude = ('user', 'timestamp', 'question', )


class AnswerCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "comment-textarea",
            "id": "answer_comment"
        }), label='')

    class Meta:
        model = AnswerComment
        exclude = ('user', 'timestamp', 'answer', )

