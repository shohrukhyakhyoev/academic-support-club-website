from django.contrib import admin
from community.models import Question, Type, Answer, QuestionComment, AnswerComment


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(Type)


