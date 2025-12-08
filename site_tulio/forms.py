from django.forms import ModelForm
from .models import Post, Troca


class FormPost(ModelForm):
    class Meta:
        model = Post
        exclude = ['usuario', 'data_criacao', 'data_atualizacao']


class FormTroca(ModelForm):
    class Meta:
        model = Troca
        exclude = ['postagem', 'usuario_interessado', 'data_criacao', 'status']