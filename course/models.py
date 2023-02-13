from tinymce import HTMLField

from django.contrib.auth import get_user_model

from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import now


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    school = models.ForeignKey(Tag, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    image = models.ImageField()
    timestamp = models.DateTimeField(default=now)
    featured = models.BooleanField(default=False)
    home = models.BooleanField(default=False)
    linked_course = models.ForeignKey(
        'self', related_name='linked', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class File(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return self.course.title + " | " + self.title


class Item(models.Model):
    title = models.CharField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    file = models.ForeignKey(File, on_delete=models.PROTECT)
    url = models.CharField(max_length=300)
    description = HTMLField(blank=True, null=True)
    attachments = HTMLField(default="Test")
    time = models.CharField(max_length=50, default="1h 35m")
    isVideo = models.BooleanField(default=False)

    def __str__(self):
        return self.course.title + " | " + self.file.title + " | " + self.title

    def get_absolute_url(self):
        return redirect(reverse('item_detail', kwargs={
            'pk': self.pk
        }))


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(default=now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return redirect(reverse('post_detail', kwargs={
            'pk': self.pk
        }))



