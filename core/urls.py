from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('produtos/', views.produtos, name='produtos'),

    # Formulário de FDS
    path('enviar-fds-form/', views.enviar_fds_form, name='enviar_fds_form'),

    # Página de contato
    path('contato/', views.contato, name='contato'),

    # Envio do formulário de contato (precisa desta rota!)
    path('enviar-contato/', views.enviar_contato, name='enviar_contato'),
]
