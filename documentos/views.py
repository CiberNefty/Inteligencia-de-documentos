from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentoForm
from .rag_utils import procesar_documento

# Create your views here.

@login_required
def subir_documento(request):
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user # <- Aqui me asigna el usuario de una vez
            documento.save()

            procesar_documento(documento)

            return redirect("lista_documentos")
    else:
        form = DocumentoForm()
    return render(request, 'documentos/subir_documento.html', {
        'form' : form
    })

@login_required
def lista_documentos(request):
    documentos = request.user.documento_set.all()
    return render(request, 'documentos/lista_documentos.html', {
        'documentos':documentos
    })