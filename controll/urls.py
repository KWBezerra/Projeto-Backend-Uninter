from django.urls import path
from . import views

urlpatterns = [
    path("prontuario/criar/", views.criar_prontuario, name="criar_prontuario"),
    path("prontuario/<int:prontuario_id>/editar/", views.editar_prontuario, name="editar_prontuario"),
    path("prontuario/agendamento/<int:agendamento_id>/", views.ver_prontuario_por_agendamento, name="ver_por_agendamento"),
    path("prontuario/historico/<str:nome_paciente>/", views.historico_paciente, name="historico_paciente"),
]
