from django.contrib import admin
from .models import Documento,Fragmento,Conversacion,Mensaje
# Register your models here.

admin.site.register(Documento)
admin.site.register(Fragmento)
admin.site.register(Conversacion)
admin.site.register(Mensaje)


