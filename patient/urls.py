from django.urls import path
from . import views # Importa as views do seu app patient

urlpatterns = [
    # URLs para Pacientes
    # patient/paciente/ (GET: listar todos, POST: cadastrar novo)
    path('paciente/', views.paciente_list_create, name='paciente_list_create'),
    # patient/paciente/{id}/ (GET: detalhar, PUT: atualizar, DELETE: remover)
    path('paciente/<int:id>/', views.paciente_detail_update_delete, name='paciente_detail_update_delete'),

    # URLs para Agendamentos
    # patient/agendamento/ (GET: listar todos, POST: agendar novo)
    path('agendamento/', views.agendamento_list_create, name='agendamento_list_create'),
    # patient/agendamento/{id}/cancelar/ (PUT: cancelar agendamento)
    path('agendamento/<int:id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
]
