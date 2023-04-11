from django.contrib import admin
from .models import Query, Article, UserDefault

admin.site.register((
    Query,
    Article,
    UserDefault
))
