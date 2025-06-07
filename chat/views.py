from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Mensagem
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

User = get_user_model()


@login_required
def chat(request, usuario_id=None):
    User = get_user_model()

    if request.user.is_superuser:
        # Usuários com quem o admin trocou mensagens
        usuarios_com_mensagens = list(
            User.objects.filter(
                id__in=Mensagem.objects.filter(destinatario=request.user)
                .values_list('remetente', flat=True)
            ).exclude(id=request.user.id)
        )
    else:
        # Usuário comum vê só o admin
        admin = User.objects.filter(is_superuser=True).first()
        usuarios_com_mensagens = [admin] if admin else []

    # Pegando o usuário selecionado
    usuario_selecionado = get_object_or_404(User, id=usuario_id) if usuario_id else usuarios_com_mensagens[0]

    # Garante que o selecionado aparece na lista
    if usuario_selecionado not in usuarios_com_mensagens:
        usuarios_com_mensagens.insert(0, usuario_selecionado)

    # Mensagens da conversa
    mensagens = Mensagem.objects.filter(
        remetente=usuario_selecionado, destinatario=request.user
    ) | Mensagem.objects.filter(
        remetente=request.user, destinatario=usuario_selecionado
    )
    mensagens = mensagens.order_by("data_envio")

    return render(request, "chat/mensagens.html", {
        "usuarios": usuarios_com_mensagens,
        "usuario_selecionado": usuario_selecionado,
        "mensagens": mensagens
    })







@csrf_exempt
@login_required
def enviar_mensagem(request, usuario_id):
    if request.method == "POST":
        conteudo = request.POST.get("conteudo")
        destinatario = get_object_or_404(User, id=usuario_id)

        if destinatario:
            mensagem = Mensagem.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                conteudo=conteudo
            )

            return JsonResponse({
                "remetente": mensagem.remetente.username,
                "destinatario": mensagem.destinatario.username,  # ✅ IMPORTANTE
                "conteudo": mensagem.conteudo,
                "data_envio": mensagem.data_envio.strftime("%H:%M")
            })

    return JsonResponse({"error": "Falha ao enviar mensagem."}, status=400)



@login_required
def buscar_usuarios(request):
    termo = request.GET.get("q", "").strip().lower()
    resultados = []

    if termo:
        usuarios = User.objects.filter(
            Q(username__icontains=termo),
            is_superuser=False
        ).exclude(id=request.user.id)[:10]

        resultados = [
            {"id": u.id, "username": u.username}
            for u in usuarios
        ]

    return JsonResponse(resultados, safe=False)
