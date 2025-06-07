from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Sum
from animais.models import Animal
from usuarios.models import Lance
from administrador.models import LogAuditoria

User = get_user_model()

@login_required
def gerenciar_usuarios(request):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('dashboard')

    usuarios = User.objects.exclude(id=request.user.id)  # Exclui o próprio admin
    return render(request, 'administrador/gerenciar_usuarios.html', {'usuarios': usuarios})

@login_required
def banir_usuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para isso.")
        return redirect("administrador:gerenciar_usuarios")

    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = False  # Desativa o usuário
    usuario.save()
    messages.success(request, f"Usuário {usuario.username} foi banido.")
    return redirect("administrador:gerenciar_usuarios")

@login_required
def desbanir_usuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para isso.")
        return redirect("administrador:gerenciar_usuarios")

    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = True  # Reativa o usuário
    usuario.save()
    messages.success(request, f"Usuário {usuario.username} foi desbanido.")
    return redirect("administrador:gerenciar_usuarios")
# 📋 Auditoria do Sistema - Apenas Administradores
@login_required
def auditoria_sistema(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    auditoria = LogAuditoria.objects.select_related('usuario').order_by('-data_hora')
    return render(request, 'administrador/auditoria.html', {'auditoria': auditoria})


# 📊 Relatórios e Estatísticas - Apenas Administradores
@login_required
def relatorios_estatisticas(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    total_usuarios = User.objects.count()
    total_animais = Animal.objects.count()
    total_lances = Lance.objects.count()
    total_faturamento = Lance.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    usuarios = User.objects.all()
    animais = Animal.objects.all()
    lances = Lance.objects.all()
    faturamento = Lance.objects.filter(animal__status='Vendido')


    context = {
        'total_usuarios': total_usuarios,
        'total_animais': total_animais,
        'total_lances': total_lances,
        'total_faturamento': total_faturamento,
        'usuarios': usuarios,  # Lista de usuários
        'animais': animais,  # Lista de animais cadastrados
        'lances': lances,  # Lista de lances realizados
        'faturamento': faturamento  # Origem do faturamento
    }

    return render(request, 'administrador/estatisticas.html', context)
