from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from animais.models import Animal
from .models import Lance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from .models import Endereco # Certifique-se de que tem um modelo chamado Endereco
from .forms import EnderecoForm  # Certifique-se de ter um formulário EnderecoForm
from entregador.models import Entregador


User = get_user_model()


def index(request):

    # Verifica se o usuário é administrador ou vendedor e redireciona para o dashboard
    if request.user.is_authenticated and (request.user.is_superuser or request.user.tipo == "vendedor"):
        return redirect("dashboard")

    # Caso contrário, exibe a home normalmente
    animais = Animal.objects.all()
    return render(request, "index.html", {"animais": animais})


def login_view(request):
    if request.method == 'POST':
        print("✅ Login solicitado!")  # Confirma que a requisição chegou

        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')
        admin_key = request.POST.get('admin_key', '')

        print(f"🔹 Usuário: {username}, Tipo: {tipo_usuario}, Chave informada: {admin_key}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("✅ Usuário autenticado com sucesso!")

            if tipo_usuario == "administrador":
                if not user.is_superuser:
                    print("⛔ Usuário não tem permissão de admin")
                    return render(request, 'login.html', {'error': '❌ Você não tem permissão de administrador.'})

                # Verifica a chave de segurança
                if admin_key.strip() != settings.ADMIN_SECRET_KEY.strip():
                    print(f"⛔ Chave incorreta! Esperado: {settings.ADMIN_SECRET_KEY}, Recebido: {admin_key}")
                    return render(request, 'login.html', {'error': '🔑 Chave de segurança incorreta.'})

            request.session['tipo_usuario'] = tipo_usuario
            login(request, user)
            print("✅ Login concluído, redirecionando para o painel")
            return redirect('dashboard')

        else:
            print("⛔ Usuário ou senha inválidos")
            return render(request, 'login.html', {'error': '❌ Usuário ou senha inválidos'})

    print("⚠️ Página de login carregada")
    return render(request, 'login.html')



@login_required
def dashboard(request):
    usuario = request.user
    tipo_usuario = request.session.get('tipo_usuario', 'comprador')  # Padrão para comprador
    
    try:
        lances = Lance.objects.filter(animal__vendedor=usuario)
        animais = Animal.objects.filter(vendedor=usuario)
    except AttributeError:
        lances = []
        animais = []
    
    return render(request, 'dashboard.html', {
        'usuario': usuario,
        'tipo_usuario': tipo_usuario,
        'lances': lances,
        'animais': animais
    })



def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario', 'comprador')  # Valor padrão 'comprador'

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'error': 'Usuário já existe'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            tipo=tipo_usuario  # Agora o tipo de usuário é salvo corretamente
        )
        login(request, user)
        return redirect('dashboard')

    return render(request, 'cadastro.html')



@login_required
def cadastrar_animal(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        raca = request.POST.get('raca', '').strip()
        peso = request.POST.get('peso', '').strip()
        idade = request.POST.get('idade', '').strip()
        status = request.POST.get('status', 'Disponível')
        imagem = request.FILES.get('imagem')
        valor_minimo = request.POST.get('valor_minimo', '').strip()

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not nome or not raca or not peso or not idade or not imagem or not valor_minimo:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('dashboard')

        # Validação de peso, idade e valor mínimo
        try:
            peso_decimal = Decimal(peso)
            idade_int = int(idade)
            valor_minimo_decimal = Decimal(valor_minimo)

            if peso_decimal <= 0 or idade_int <= 0 or valor_minimo_decimal <= 0:
                raise ValueError
        except (ValueError, InvalidOperation):
            messages.error(request, "Peso, idade e valor mínimo devem ser números positivos e válidos.")
            return redirect('dashboard')

        # Criando o objeto no banco de dados
        Animal.objects.create(
            nome=nome,
            raca=raca,
            peso=peso_decimal,
            idade=idade_int,
            vendedor=request.user, 
            imagem=imagem,
            status=status,
            valor_minimo=valor_minimo_decimal
        )

        messages.success(request, "Animal cadastrado com sucesso!")
        return redirect('dashboard')

    return render(request, 'dashboard.html')


def atualizar_ranking(request, animal_id):
    lances = Lance.objects.filter(animal_id=animal_id).order_by('-valor')[:5]  # Os 5 maiores lances
    ranking_data = [
        {"comprador": lance.comprador.username, "valor": lance.valor} for lance in lances
    ]
    return JsonResponse(ranking_data, safe=False)

def buscar_vencedor(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    # Pegando o maior lance associado ao animal
    maior_lance = Lance.objects.filter(animal=animal).order_by('-valor').first()

    if maior_lance:
        return JsonResponse({"vencedor": maior_lance.comprador.username, "valor": str(maior_lance.valor)})
    else:
        return JsonResponse({"vencedor": None})

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def admin_dashboard(request):
    if request.user.tipo_usuario != "administrador":
        return redirect('index')  # Bloqueia acesso de não administradores

    return render(request, 'dashboard.html', {
        'usuarios': User.objects.all()
    })


@login_required
def salvar_endereco(request):
    try:
        endereco = Endereco.objects.get(usuario=request.user)
    except Endereco.DoesNotExist:
        endereco = None

    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            return redirect('dashboard')  # Redireciona para o dashboard ou outra página

    else:
        form = EnderecoForm(instance=endereco)

    return render(request, 'endereco_form.html', {'form': form})


def checkout(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    lance_vencedor = Lance.objects.filter(animal=animal).order_by('-valor').first()
    entregadores = Entregador.objects.all()

    return render(request, 'checkout.html', {
        'animal': animal,
        'lance': lance_vencedor,
        'entregadores': entregadores  # agora presente também aqui
    })
