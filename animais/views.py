from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal
from decimal import Decimal, InvalidOperation
from usuarios.models import Lance
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q



@login_required
def animal_detalhes(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    
    # Mostrar lances apenas para o dono do animal
    lances = Lance.objects.filter(animal=animal).order_by('-valor') if animal.vendedor == request.user else []

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redireciona se o usuário não estiver logado

        valor = request.POST.get('valor_manual', '').strip()

        try:
            valor = Decimal(valor)
            if valor <= 0:
                raise ValueError
        except (ValueError, InvalidOperation):
            return render(request, 'animais/animal_detalhes.html', {
                'animal': animal,
                'lances': lances,
                'error': 'O valor do lance deve ser um número positivo válido.'
            })

        # Criar o lance no banco de dados
        Lance.objects.create(animal=animal, comprador=request.user, valor=valor)
        return redirect('animal_detalhes', animal_id=animal.id)

    return render(request, 'animais/animal_detalhes.html', {'animal': animal, 'lances': lances})



def aceitar_lance(request, lance_id):
    lance = get_object_or_404(Lance, id=lance_id)

    # Atualiza o status do lance para aceito
    lance.status = 'aceito'
    lance.save()

    # Garante que o comprador tenha uma sessão válida para armazenar a mensagem
    if lance.comprador and lance.comprador.is_authenticated:
        request.session['mensagem_lance'] = (
            f"Seu lance de R$ {lance.valor} foi aceito! "
            f"<a href='{reverse('pagamentos:checkout')}'>Clique aqui para finalizar a compra</a>."
        )

    return redirect('dashboard')

def rejeitar_lance(request, lance_id):
    lance = get_object_or_404(Lance, id=lance_id)

    # Atualiza o status do lance para rejeitado
    lance.status = 'rejeitado'
    lance.save()

    # Garante que o comprador tenha uma sessão válida para armazenar a mensagem
    if lance.comprador and lance.comprador.is_authenticated:
        request.session['mensagem_lance'] = "Seu lance foi rejeitado. Você pode tentar novamente com outro valor."

    return redirect('dashboard')


def buscar_animais(request):
    query = request.GET.get('q', '').strip().lower()

    if request.user.is_authenticated:
        # Usuários logados veem apenas animais que não são deles
        animais = Animal.objects.filter(nome__icontains=query).exclude(vendedor=request.user)
    else:
        # Usuários não logados veem todos os animais
        animais = Animal.objects.filter(nome__icontains=query)

    # Retorna apenas os dados necessários
    data = list(animais.values("id", "nome", "raca"))
    
    return JsonResponse(data, safe=False)