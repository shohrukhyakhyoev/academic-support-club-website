from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include

from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

from community.views import (
    register,
    spaces,
    questions,
    question,
    create_question,
    update_question,
    update_answer
)

from course.views import (
    index,
    tutorials,
    tutorial,
    news,
    about,
    contact,
    ItemDetailView,
    PostDetailView,
    create_post,
    update_post,
    delete_post,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthForm), name='login'),
    path('community/signup/', register, name='signup'),
    path('community/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tinymce/', include('tinymce.urls')),

    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('community/spaces/', spaces, name='spaces'),

    path('community/questions/', questions, name='questions'),
    path('community/question/ask/', create_question, name='question_create'),
    path('community/question/<pk>/', question, name='question'),
    path('community/question/<pk>/update/', update_question, name='question_update'),
    path('community/answer/<pk>/update/', update_answer, name='answer_update'),

    path('tutorial/', tutorials, name='tutorial'),
    path('material/<pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('tutorial/<id>/', tutorial, name="tutorial_detail"),

    path('news/', news, name='news'),
    path('news/create/', create_post, name='post_create'),
    path('news/<pk>/', PostDetailView.as_view(), name='post_detail'),
    path('news/<pk>/update/', update_post, name='post_update'),
    path('news/<pk>/delete/', delete_post, name='post_delete')

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
