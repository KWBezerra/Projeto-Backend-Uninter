from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from .models import Prontuario
from patient.models import Agendamento
from register.models import Funcionario

@csrf_exempt
@login_required
def criar_prontuario(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            agendamento = Agendamento.objects.get(id=data["agendamento_id"])
        except Agendamento.DoesNotExist:
            return JsonResponse({"erro": "Agendamento não encontrado"}, status=404)

        prontuario = Prontuario.objects.create(
            agendamento=agendamento,
            paciente_nome=data["paciente_nome"],
            idade=data["idade"],
            data_consulta=data["data_consulta"],
            queixa_principal=data["queixa_principal"],
            historia_clinica=data["historia_clinica"],
            antecedentes=data.get("antecedentes"),
            medicacoes=data.get("medicacoes"),
            pa=data.get("pa"),
            fc=data.get("fc"),
            ausculta=data.get("ausculta"),
            impressao_diagnostica=data["impressao_diagnostica"],
            conduta=data["conduta"],
            medico_nome=data["medico_nome"],
            medico_crm=data["medico_crm"],
            criado_por=request.user.funcionario
        )

        return JsonResponse({"mensagem": "Prontuário criado com sucesso", "id": prontuario.id}, status=201)

@csrf_exempt
@login_required
def editar_prontuario(request, prontuario_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        prontuario = get_object_or_404(Prontuario, id=prontuario_id)

        for campo in [
            "queixa_principal", "historia_clinica", "antecedentes", "medicacoes",
            "pa", "fc", "ausculta", "impressao_diagnostica", "conduta"
        ]:
            if campo in data:
                setattr(prontuario, campo, data[campo])

        prontuario.save()
        return JsonResponse({"mensagem": "Prontuário atualizado com sucesso"})

@login_required
def ver_prontuario_por_agendamento(request, agendamento_id):
    prontuario = get_object_or_404(Prontuario, agendamento__id=agendamento_id)
    return JsonResponse({
        "paciente": prontuario.paciente_nome,
        "data_consulta": prontuario.data_consulta,
        "diagnostico": prontuario.impressao_diagnostica,
        "conduta": prontuario.conduta,
        "medico": prontuario.medico_nome,
    })

@login_required
def historico_paciente(request, nome_paciente):
    prontuarios = Prontuario.objects.filter(paciente_nome__icontains=nome_paciente).order_by("-data_consulta")

    lista = [
        {
            "data": p.data_consulta,
            "diagnostico": p.impressao_diagnostica,
            "medico": p.medico_nome,
        }
        for p in prontuarios
    ]

    return JsonResponse({"historico": lista})
