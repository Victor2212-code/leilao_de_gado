from django.shortcuts import render, get_object_or_404
from animais.models import Animal
from usuarios.models import Lance  # Certifique-se de importar corretamente
import qrcode
from io import BytesIO
from django.http import HttpResponse
from entregador.models import Entregador

def checkout(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    # Pegando o maior lance, sem precisar de status de aprovação
    lance_vencedor = Lance.objects.filter(animal=animal).order_by('-valor').first()
    
    entregadores = Entregador.objects.all()

    return render(request, 'checkout.html', {
        'animal': animal,
        'lance': lance_vencedor,
        'entregadores': entregadores, # Passando o maior lance diretamente
        'is_checkout': True
    })



def gerar_qrcode(request):
    # Código fictício PIX (pode ser um código aleatório para testes)
    pix_code = "00020126360014BR.GOV.BCB.PIX0114+5561987654320520400005303986540510005802BR5924Nome Exemplo da Conta6012Brasilia7003***6304ABCD"

    # Criando o QR Code
    qr = qrcode.make(pix_code)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    # Retorna a imagem como resposta HTTP
    return HttpResponse(buffer.getvalue(), content_type="image/png")




def finalizar_compra(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    
    # Pega o lance aprovado mais alto (ou use sua lógica específica)
    lance = Lance.objects.filter(animal=animal, status='Aprovado').order_by('-valor').first()

    # ✅ Aqui está o ponto principal: buscar todos os entregadores
    entregadores = Entregador.objects.all()

    return render(request, 'checkout.html', {
        'animal': animal,
        'lance': lance,
        'entregadores': entregadores  # <-- variável essencial para o template
    })