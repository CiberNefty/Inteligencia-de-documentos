from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_documento, name='subir_documento'),
    path('', views.lista_documentos, name="lista_documentos"),
]

