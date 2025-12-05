from django.shortcuts import render, redirect
from .forms import FormPost
from .models import Post
from django.views.generic import ListView, DeleteView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

#cria a classe novoPost para gerenciar as funções de postagem usando atributos de classe para armazenar os posts em memória
class criarPost(LoginRequiredMixin, View):
    login_url = '/contas/login/'
    model = Post
    classe_form = FormPost
    name_template = 'postar.html'

    def get(self, request):
        formulario = self.classe_form()
        return render(request, self.name_template, {'formulario': formulario})

    def post(self, request):
        formulario = self.classe_form(request.POST, request.FILES)
        if formulario.is_valid():
            post = formulario.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('inicio')
        return render(request, self.name_template, {'formulario': formulario})

class listarPost(LoginRequiredMixin, ListView):
    login_url = '/contas/login/'
    model = Post
    template_name = "inicio.html"
    context_object_name = 'posts'
    ordering = ['-id']


from django.urls import reverse_lazy

class deletarPost(LoginRequiredMixin, DeleteView):
    login_url = '/contas/login/'
    model = Post
    template_name = "confirmar_delete.html"
    success_url = reverse_lazy('inicio')

    def get_queryset(self):
        # somente o autor pode deletar
        qs = super().get_queryset()
        return qs.filter(autor=self.request.user)

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