from django.contrib import admin
from .models import Post, Usuario, Troca

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ('user', 'nome_completo', 'data_criacao')
	search_fields = ('user__username', 'nome_completo')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'titulo', 'usuario', 'habilidade_oferecida', 'ativa', 'data_criacao')
	list_filter = ('ativa', 'data_criacao')
	search_fields = ('titulo', 'descricao', 'habilidade_oferecida', 'usuario__user__username')

@admin.register(Troca)
class TrocaAdmin(admin.ModelAdmin):
	list_display = ('id', 'postagem', 'usuario_interessado', 'habilidade_proposta', 'status', 'data_criacao')
	list_filter = ('status',)
	search_fields = ('postagem__titulo', 'usuario_interessado__user__username')