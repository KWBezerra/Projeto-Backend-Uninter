from django.urls import path
from . import views

urlpatterns = [
    path('paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('agendamento/', views.marcar_agendamento, name='marcar_agendamento'),
    path('agendamento/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
]
