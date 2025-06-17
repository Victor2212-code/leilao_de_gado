from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Entregador, Entrega
from usuarios.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login
from decimal import Decimal


def cadastro_entregador(request):
    return render(request, 'cadastro_entregador.html')


Usuario = get_user_model()


def salvar_entregador(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Usuario.objects.filter(username=username).exists():
            return render(request, 'cadastro_entregador.html', {
                'error': '⚠️ Este nome de usuário já está em uso.'
            })

        # Criação do usuário com tipo entregador
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        usuario.tipo = 'entregador'
        usuario.save()

        # Criação do entregador vinculado ao usuário
        Entregador.objects.create(
            usuario=usuario,
            nome=request.POST.get('nome'),
            placa=request.POST.get('placa'),
            tipo_preco=request.POST.get('tipo_preco'),
            valor=Decimal(request.POST.get('valor')),
            cpf=request.POST.get('cpf'),
            pix=request.POST.get('pix'),
            telefone=request.POST.get('telefone'),
        )

        messages.success(request, "✅ Entregador cadastrado com sucesso!")
        return redirect('login')

    return render(request, 'cadastro_entregador.html')



@login_required
def salvar_endereco(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.endereco = request.POST['endereco']
        usuario.cep = request.POST['cep']
        usuario.estado = request.POST['estado']
        usuario.telefone = request.POST['telefone']
        usuario.save()
    return redirect('dashboard')

@login_required
def visualizar_entregas(request):
    entregador = getattr(request.user, 'entregador', None)
    if not entregador:
        messages.error(request, "❌ Seu perfil de entregador não está completo.")
        return redirect('dashboard')

    entregas = entregador.entrega_set.all()
    return render(request, 'visualizar_entregas.html', {'entregas': entregas})


@login_required
def aceitar_entrega(request):
    entregador = getattr(request.user, 'entregador', None)
    if not entregador:
        messages.error(request, "❌ Seu perfil de entregador não está completo.")
        return redirect('dashboard')

    entregas_disponiveis = Entrega.objects.filter(status='pendente')

    if request.method == 'POST':
        entrega_id = request.POST.get('entrega_id')
        entrega = get_object_or_404(Entrega, id=entrega_id)
        entrega.entregador = entregador
        entrega.status = 'aceita'
        entrega.save()
        messages.success(request, "✅ Entrega aceita com sucesso!")
        return redirect('entregador:visualizar_entregas')

    return render(request, 'aceitar_entrega.html', {'entregas': entregas_disponiveis})


@login_required
def confirmar_entrega(request):
    entregador = getattr(request.user, 'entregador', None)
    if not entregador:
        messages.error(request, "❌ Seu perfil de entregador não está completo.")
        return redirect('dashboard')

    entregas_ativas = Entrega.objects.filter(entregador=entregador, status='aceita')

    if request.method == 'POST':
        entrega_id = request.POST.get('entrega_id')
        entrega = get_object_or_404(Entrega, id=entrega_id, entregador=entregador)
        entrega.status = 'confirmada'
        entrega.save()
        messages.success(request, "✅ Entrega confirmada com sucesso!")
        return redirect('entregador:visualizar_entregas')

    return render(request, 'confirmar_entrega.html', {'entregas': entregas_ativas})


@login_required
def atualizar_dados(request):
    entregador = getattr(request.user, 'entregador', None)
    if not entregador:
        messages.error(request, "❌ Seu perfil de entregador ainda não foi criado.")
        return redirect('dashboard')

    if request.method == 'POST':
        entregador.nome = request.POST.get('nome')
        entregador.placa = request.POST.get('placa')
        entregador.tipo_preco = request.POST.get('tipo_preco')
        entregador.valor = request.POST.get('valor')
        entregador.cpf = request.POST.get('cpf')
        entregador.pix = request.POST.get('pix')
        entregador.telefone = request.POST.get('telefone')
        entregador.save()
        messages.success(request, "✅ Dados atualizados com sucesso!")
        return redirect('dashboard')

    return render(request, 'atualizar_dados.html', {'entregador': entregador})
