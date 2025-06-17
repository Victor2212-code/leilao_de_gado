"""
URL configuration for leilao_gado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from animais.viewsets import AnimalViewSet
from pagamentos.viewsets import TransacaoViewSet
from usuarios.viewsets import UsuarioViewSet, AvaliacaoViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'animais', AnimalViewSet)
router.register(r'transacoes', TransacaoViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('animais/', include('animais.urls')),
    path('', include('usuarios.urls')),
    path('pagamentos/', include('pagamentos.urls', namespace='pagamentos')),
    path('admin_system/',include('administrador.urls',namespace='administrador')),
    path('chat/',include('chat.urls', namespace='chat')),
    path('entregador/',include('entregador.urls', namespace='entregador')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)