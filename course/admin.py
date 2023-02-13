from django.contrib import admin
from .models import Author, Tag, Course, Category, Post, File, Item


# Register your models here.
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(File)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Post)




