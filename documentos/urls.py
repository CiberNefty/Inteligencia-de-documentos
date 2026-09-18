from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_documento, name='subir_documento'),
    path('<int:documento_id>/chat/', views.chat_documento, name="chat_documento"),
    path('', views.lista_documentos, name="lista_documentos"),
]

