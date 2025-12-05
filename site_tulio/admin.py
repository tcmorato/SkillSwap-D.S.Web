from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'autor')
	search_fields = ('titulo', 'descricao', 'autor__username')
