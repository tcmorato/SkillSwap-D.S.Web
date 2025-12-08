from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormPost, FormTroca
from .models import Post, Troca, Usuario
from django.views.generic import ListView, DeleteView, View, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

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
            post.usuario = request.user.perfil
            post.save()
            return redirect('inicio')
        return render(request, self.name_template, {'formulario': formulario})

class listarPost(LoginRequiredMixin, ListView):
    login_url = '/contas/login/'
    model = Post
    template_name = "inicio.html"
    context_object_name = 'posts'
    ordering = ['-data_criacao']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context.get('posts')
        if posts:
            for post in posts:
                post.accepted_troca = post.trocas.filter(status='aceita').first()
        return context


from django.urls import reverse_lazy

class deletarPost(LoginRequiredMixin, DeleteView):
    login_url = '/contas/login/'
    model = Post
    template_name = "confirmar_delete.html"
    success_url = reverse_lazy('inicio')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(usuario__user=self.request.user)

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


def logout_simples(request):
    logout(request)
    return redirect('login')

class editarPost(LoginRequiredMixin, UpdateView):
    login_url = '/contas/login/'
    model = Post
    template_name = 'postar.html'
    success_url = reverse_lazy('inicio')
    form_class = FormPost

    def get_queryset(self):
        qs = super().get_queryset() 
        return qs.filter(usuario__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulario'] = context.get('form')
        return context
    
def solicitar_troca(request, pk):
    postagem = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = FormTroca(request.POST, request.FILES)
        if form.is_valid():
            troca = form.save(commit=False)
            troca.postagem = postagem
            troca.usuario_interessado = request.user.perfil
            troca.save()
            return redirect('inicio')
    else:
        form = FormTroca()
    return render(request, 'solicitar_troca.html', {'form': form, 'postagem': postagem})


@login_required(login_url='/contas/login/')
def perfil(request):
    perfil = request.user.perfil
    trocas_recebidas = Troca.objects.filter(postagem__usuario=perfil).order_by('-data_criacao')
    return render(request, 'perfil.html', {'perfil': perfil, 'trocas_recebidas': trocas_recebidas})


@login_required(login_url='/contas/login/')
def aceitar_troca(request, pk):
    troca = get_object_or_404(Troca, pk=pk)
    if troca.postagem.usuario.user != request.user:
        return redirect('perfil')
    troca.status = 'aceita'
    troca.save()
    return redirect('perfil')


@login_required(login_url='/contas/login/')
def recusar_troca(request, pk):
    troca = get_object_or_404(Troca, pk=pk)
    if troca.postagem.usuario.user != request.user:
        return redirect('perfil')
    troca.status = 'recusada'
    troca.save()
    return redirect('perfil')