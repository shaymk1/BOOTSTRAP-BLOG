from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  list_filter = ("title", "author")
  list_display = ("title", "overview", "author", "timestamp")
  prepopulated_fields = {"slug": ("title",)}

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
