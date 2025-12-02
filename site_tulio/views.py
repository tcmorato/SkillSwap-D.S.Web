from django.shortcuts import render,redirect
from .forms import FormPost
from .models import Post
from django.views.generic import ListView, DeleteView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

#cria a classe novoPost para gerenciar as funções de postagem usando atributos de classe para armazenar os posts em memória
class criarPost(View):
    model = Post
    classe_form = FormPost
    name_template = 'postar.html'

    def get(self, request):
        formulario = self.classe_form()
        return render(request, self.name_template, {'formulario':formulario})

    def post(self, request):
        formulario = self.classe_form(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('inicio')
        return render(request, self.name_template, {'formulario':formulario})

class listarPost(ListView):
    model = Post
    template_name = "inicio.html"
    context_object_name = 'posts'
    ordering = ['-id']


from django.urls import reverse_lazy

class deletarPost(DeleteView):
    model = Post
    template_name = "confirmar_delete.html"
    success_url = reverse_lazy('inicio')

    from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})