from django.contrib import admin
from user.models import CustomUser

from .models import Category, Comment, Genre, Review, Title

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
