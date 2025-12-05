from django.forms import ModelForm
from .models import Post

class FormPost(ModelForm):
    class Meta:
        model = Post
        # autor será atribuído automaticamente ao usuário logado
        exclude = ['autor']