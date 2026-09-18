from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentoForm
from .rag_utils import procesar_documento, buscar_fragmentos_relevantes, generar_respuesta_chat
from .models import Documento, Conversacion, Mensaje



# Create your views here.

@login_required
def subir_documento(request):
    error_documento = None
    
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user # <- Aqui me asigna el usuario de una vez
            documento.save()

            try:                   
                procesar_documento(documento)
                return redirect("lista_documentos") #<- Solo redirige sso NO hubo error
            except Exception as e:
                error_documento = str(e) # <- 
    else:
        form = DocumentoForm()
    return render(request, 'documentos/subir_documento.html', {
        'form' : form, 
        "error_documento":error_documento
    })

@login_required
def lista_documentos(request):
    documentos = request.user.documento_set.all()
    return render(request, 'documentos/lista_documentos.html', {
        'documentos':documentos
    })

@login_required
def chat_documento(request, documento_id):
    documento = Documento.objects.get(id=documento_id, usuario=request.user)

    conversacion, creada = Conversacion.objects.get_or_create(
        documento=documento,
        usuario=request.user,
        defaults={'titulo': f"Chat sobre {documento.titulo}"}
    )

    error = None

    if request.method == 'POST':
        pregunta = request.POST.get('pregunta').strip()

        if not pregunta:
            error = "Escribi una pregunta antes de enviar."
        else:    
            Mensaje.objects.create(conversacion=conversacion, rol='user', contenido=pregunta)
            try:
                fragmentos = buscar_fragmentos_relevantes(documento, pregunta)
                respuesta_texto = generar_respuesta_chat(pregunta, fragmentos)
            except Exception as e:
                respuesta_texto = "Hubo un poblema generando la respuesta. Intenta de nuevo en un momento."
                
            Mensaje.objects.create(conversacion=conversacion, rol='assistant', contenido=respuesta_texto)
            return redirect('chat_documento', documento_id=documento.id)

    mensajes = conversacion.mensajes.all().order_by('fecha_creacion')

    return render(request, 'documentos/chat.html', {
        'documento': documento,
        'mensajes': mensajes,
        'error': error
    })