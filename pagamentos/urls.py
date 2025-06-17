from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('checkout/<int:animal_id>/', views.checkout, name='checkout'),
    path('gerar_qrcode/', views.gerar_qrcode, name='gerar_qrcode'),
]
