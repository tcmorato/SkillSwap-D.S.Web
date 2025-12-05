from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
    )
    titulo = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='imagens/')
    descricao = models.TextField()

    def __str__(self) -> str:
        autor = self.autor.username if self.autor else '—'
        return f"{self.titulo} (por {autor})"