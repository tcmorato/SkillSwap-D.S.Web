from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name ='perfil'
    )
    nome_completo = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True, default='')
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        related_name = 'posts',
    )
    titulo = models.CharField(max_length=200, blank=True, default='')
    habilidade_oferecida = models.CharField(max_length=150, blank=True, default='')
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True, default='')
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativa = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.titulo} (por {self.usuario})"
    
class Troca(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('recusada', 'Recusada'),
        ('cancelada', 'Cancelada'),
    ]

    postagem = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'trocas'
    )

    usuario_interessado = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        related_name = 'trocas_feitas'
    )

    habilidade_proposta = models.CharField(max_length=150, blank=True, default='')
    mensagem = models.TextField(max_length=500, blank=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    video_proposto = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self) -> str:
        return f"Troca #{self.pk} para {self.postagem.titulo} por {self.usuario_interessado}"
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.get_or_create(user=instance)