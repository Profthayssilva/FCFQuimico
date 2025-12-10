from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('produtos/', views.produtos, name='produtos'),
    path('enviar-fds-form/', views.enviar_fds_form, name='enviar_fds_form'),
    path('contato/', views.contato, name='contato'),
]
