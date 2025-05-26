import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paciente, Agendamento
from django.shortcuts import get_object_or_404

@csrf_exempt
def cadastrar_paciente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paciente = Paciente.objects.create(
            nome_completo=data['nome_completo'],
            cpf=data['cpf'],
            data_nascimento=data['data_nascimento'],
            celular=data['celular']
        )
        return JsonResponse({'mensagem': 'Paciente cadastrado com sucesso!', 'id': paciente.id})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def marcar_agendamento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paciente = get_object_or_404(Paciente, id=data['paciente_id'])
        agendamento = Agendamento.objects.create(
            paciente=paciente,
            data_hora=data['data_hora'],
            tipo=data['tipo'],
            especialidade=data['especialidade']
        )
        return JsonResponse({'mensagem': 'Agendamento realizado com sucesso!', 'id': agendamento.id})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def cancelar_agendamento(request, agendamento_id):
    if request.method == 'DELETE':
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        agendamento.delete()
        return JsonResponse({'mensagem': 'Agendamento cancelado com sucesso!'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
