from markdownx.admin import MarkdownxModelAdmin
from django.contrib import admin
from .models import Person, Post, Question, Answer
from draceditor.widgets import AdminDraceditorWidget
from django.db import models

admin.site.register(Person)
admin.site.register(Question)
admin.site.register(Answer)

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminDraceditorWidget},
    }

admin.site.register(Post, PostAdmin)
# Register your models here.
