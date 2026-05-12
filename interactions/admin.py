from django.contrib import admin
from .models import Bookmark, Clap, Follow, Report

admin.site.register(Bookmark)
admin.site.register(Clap)
admin.site.register(Follow)
admin.site.register(Report)
