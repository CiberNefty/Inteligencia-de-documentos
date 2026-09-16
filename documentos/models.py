from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField

class Documento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    area = models.CharField(max_length=50, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Fragmento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='fragmentos')
    contenido = models.TextField()
    embedding = VectorField(dimensions=384)
    order = models.IntegerField()

    def __str__(self):
        return f"Fragmento {self.order} de {self.documento.titulo}"

class Conversacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f"Conversacion #{self.id}"

class Mensaje(models.Model):
    ROL_CHOICES = [
        ('user','Usuario'),
        ('assistant', 'Asistente'),
    ]
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rol}: {self.contenido[:50]}"