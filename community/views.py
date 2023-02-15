from itertools import chain
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from community.models import Question, Answer, QuestionComment, AnswerComment, Type
from community.forms import QuestionForm, AnswerForm, QuestionCommentForm, AnswerCommentForm
from config.forms import CustomRegistrationForm


def register(request):
    form = CustomRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Added.")

                return redirect('questions')

    return render(request, 'registration/signup.html', {"form": form})


# def spaces(request):
#     queryset = Question.objects.all().order_by('-timestamp')
#     return render(request, 'spaces.html', {"questions": queryset})


def questions(request):
    queryset = Question.objects.all().order_by('-timestamp')
    tags = Type.objects.all()[0:10]

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(tag__title__icontains=search_query)
        ).distinct()

    tag_request_var = 'tag'
    tag_search_query = request.GET.get(tag_request_var, '')
    if tag_search_query != '' and tag_search_query != 'Latest':
        if tag_search_query == 'Active':
            queryset = [obj for obj in queryset if obj.is_active()]
        elif tag_search_query == 'Unanswered':
            queryset = [obj for obj in queryset if not obj.has_answer()]
        else:
            queryset = [obj for obj in queryset if obj.has_answer()]

    paginator = Paginator(queryset, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        "questions": paginated_queryset,
        "page_request_var": page_request_var,
        "search_request_var": search_request_var,
        "search_query": search_query,
        "tag_request_var": tag_request_var,
        "tag_search_query": tag_search_query,
        "tags": tags
    }

    return render(request, 'community_forum.html', context)


def question(request, pk):
    obj = get_object_or_404(Question, id=pk)

    question_comment_form = QuestionCommentForm(request.POST or None)
    answer_comment_form = AnswerCommentForm(request.POST or None)
    answer_form = AnswerForm(request.POST or None)

    context = {
        'question_comment_form': question_comment_form,
        'answer_comment_form': answer_comment_form,
        'answer_form': answer_form,
        'question': obj
    }

    if not request.user.is_authenticated:
        context["login_required"] = "You have to be logged in"

    else:
        if request.method == "POST":
            if "questionComment" in request.POST:
                if question_comment_form.is_valid():
                    question_comment_id = request.POST["question_comment_id"]
                    if question_comment_id != "":
                        # TODO consider scenario if obj not found
                        question_comment = get_object_or_404(QuestionComment, id=int(question_comment_id))
                        if question_comment.user == request.user:
                            question_comment.text = question_comment_form.instance.text
                            question_comment.save()
                        else:
                            context['authority_error'] = "You cannot edit other users' comments!"
                    else:
                        question_comment_form.instance.user = request.user
                        question_comment_form.instance.question = obj
                        question_comment_form.save()

            elif "answer_id" in request.POST:
                if answer_comment_form.is_valid():
                    answer_comment_id = request.POST["answer_comment_id"]
                    if answer_comment_id != "":
                        answer_comment = get_object_or_404(AnswerComment, id=int(answer_comment_id))
                        if answer_comment.user == request.user:
                            answer_comment.text = answer_comment_form.instance.text
                            answer_comment.save()
                        else:
                            context['authority_error'] = "You cannot edit other users' comments!"
                    else:
                        answer_id = request.POST["answer_id"]
                        # TODO consider scenario if obj not found
                        answer = get_object_or_404(Answer, id=int(answer_id))
                        answer_comment_form.instance.user = request.user
                        answer_comment_form.instance.answer = answer
                        answer_comment_form.save()

            else:
                if answer_form.is_valid():
                    answer_pk = request.POST["answer_pk"]
                    # TODO consider scenario if obj not found
                    if not answer_pk:
                        if request.user != obj.user:
                            answer_form.instance.user = request.user
                            answer_form.instance.question = obj
                            answer_form.save()
                        else:
                            context["authority_error"] = "You are not permitted to answer to your own questions!"
                    else:
                        answer = get_object_or_404(Answer, id=int(answer_pk))
                        answer.content = answer_form.instance.content
                        answer.save()

            return redirect(reverse("question", kwargs={
                'pk': obj.pk
            }))

    return render(request, 'question_detail.html', context)


def create_question(request):
    form = QuestionForm(request.POST, request.FILES or None)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a question."      
    else:
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.pk
                }))
            else:
                context["error"] = form.errors

    return render(request, 'question_create.html', context)


def update_question(request, pk):
    obj = get_object_or_404(Question, id=pk)
    form = QuestionForm(request.POST or None, instance=obj)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to request for an update of question."
    elif request.user != obj.user:
        context["authority_error"] = "Bad Request: Question belongs to another user. Thus, you are not " \
                                     "allowed to edit this question."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.pk
                }))
            else:
                context["error"] = form.errors

    return render(request, 'question_update.html', context)


def update_answer(request, pk):
    obj = get_object_or_404(Answer, id=pk)
    form = AnswerForm(request.POST or None, instance=obj)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to request for an update of question."
    elif request.user == obj.question.user:
        context["authority_error"] = "Bad Request: You are not allowed to answer to your own questions."
    elif request.user != obj.user:
        context["authority_error"] = "Bad Request: Answer belongs to another user. Thus, you are not " \
                                     "allowed to edit this question."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.question.pk
                }))
            else:
                context["error"] = form.errors

    return render(request, 'answer_update.html', context)



