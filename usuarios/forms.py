from django import forms
from .models import Endereco

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'estado', 'cidade', 'bairro', 'rua', 'numero', 'complemento', 'telefone', 'cpf']
        widgets = {
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(99) 99999-9999'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }
