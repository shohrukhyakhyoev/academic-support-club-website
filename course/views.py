from itertools import chain

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView

from community.models import Question
from course.forms import PostForm
from course.models import Course, Post, Category, Tag, Item, File, Author


def get_author(user):
    lst = Author.objects.filter(id=user.id)
    return lst[0] if lst else None


def get_filters():
    categories = Category.objects.all()
    schools = Tag.objects.all()
    return list(chain(categories, schools))


def paginate_objects(request, queryset, num):
    paginator = Paginator(queryset, num)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def index(request):
    subjects = Course.objects.all()
    featured = subjects.filter(featured=True)
    latest = subjects.order_by('-timestamp')[0:3]
    extra = subjects.filter(Q(featured=True) | Q(home=True)).distinct()
    posts = Post.objects.order_by('-timestamp')[0:3]
    questions = Question.objects.order_by('-timestamp')[0:3]

    context = {
        'featured': featured,
        'posts': posts,
        'latest': latest,
        'extra': extra,
        'filters': get_filters(),
        'questions': questions
    }

    return render(request, 'index.html', context)


def tutorials(request):
    subjects = Course.objects.order_by('-timestamp')
    featured = subjects.filter(Q(featured=True) | Q(home=True)).distinct()

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_query:
        subjects = subjects.filter(
            Q(title__icontains=search_query) |
            Q(category__title__icontains=search_query) |
            Q(school__title__icontains=search_query)
        ).distinct()

    subjects = paginate_objects(request, subjects, 3)

    context = {
        'tutorials': subjects,
        'featured': featured,
        'page_request_var': 'page',
        'search_request_var': search_request_var,
        'search_query': search_query,
        'filters': get_filters()
    }

    return render(request, 'tutorials.html', context)


def tutorial(request, id):
    subject = get_object_or_404(Course, id=id)
    files = File.objects.filter(course_id=subject.id)
    materials = Item.objects.filter(course_id=subject.id)
    related = Course.objects.filter(linked_course_id=subject.id)
    featured = related[0:3]

    related = paginate_objects(request, related, 3)

    context = {
        'subject': subject,
        'files': files,
        'materials': materials,
        'related': related,
        'featured': featured,
        'page_request_var': 'page'
    }

    return render(request, 'tutorial-single.html', context)


def news(request):
    posts = Post.objects.order_by('-timestamp')

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_request_var:
        posts = posts.filter(title__icontains=search_query)

    posts = paginate_objects(request, posts, 6)

    context = {
        'posts': posts,
        'page_request_var': 'page',
        'search_request_var': search_request_var,
        'search_query': search_query
    }

    return render(request, 'blog.html', context)


def create_post(request):
    form = PostForm(request.POST, request.FILES or None)
    context = {"form": form}
    author = get_author(request.user)

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to create a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                form.save()
                return redirect(reverse("post_detail", kwargs={
                    'pk': form.instance.pk
                }))
            else:
                context["error"] = form.errors

    return render(request, 'post_create.html', context)


def update_post(request, pk):
    obj = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=obj)
    context = {"form": form}
    author = get_author(request.user)

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to edit a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create/edit/delete a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    elif request.user != obj.author.user:
        context["authority_error"] = "Bad Request: Blog post belongs to another user. Thus, you are not " \
                                     "allowed to edit this post."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse("post_detail", kwargs={
                    'pk': form.instance.pk
                }))
            else:
                context["error"] = form.errors

    return render(request, 'post_update.html', context)


def delete_post(request, pk):
    post = Post.objects.filter(id=pk)[0]
    author = get_author(request.user)
    context = {
        "post": post
    }

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a request to delete a post."
    elif not request.user.is_staff:
        context["authority_error"] = "Bad Request: You are not authorized to create/edit/delete a blog post."
    elif not author:
        context["authority_error"] = "Bad Request: You are not given permission to create/edit/delete a blog post."
    elif request.user != post.author.user:
        context["authority_error"] = "Bad Request: Blog post belongs to another user. Thus, you are not " \
                                     "allowed to delete this post."
    else:
        if request.method == "POST":
            post.delete()
            return redirect(reverse("news"))

    return render(request, 'post_delete.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'sidebar.html'

    def get_context_data(self, **kwargs):
        material = self.get_object()
        files = File.objects.filter(course_id=material.course_id)
        materials = Item.objects.filter(course_id=material.course_id)
        context = super().get_context_data(**kwargs)
        context['item'] = material
        context['materials'] = materials
        context['files'] = files
        return context

