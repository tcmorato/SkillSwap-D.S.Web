from django.forms import ModelForm
from .models import Post

class FormPost(ModelForm):
    class Meta:
        model = Post
        exclude = ['autor']