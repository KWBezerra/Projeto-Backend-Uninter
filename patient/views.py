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

@csrf_exempt
def paciente_list_create(request):
    """
    Lista todos os pacientes (GET) ou cadastra um novo paciente (POST).
    """
    if request.method == 'GET':
        pacientes = Paciente.objects.all()
        # Serializa a lista de pacientes para JSON
        pacientes_data = []
        for paciente in pacientes:
            pacientes_data.append({
                'id': paciente.id,
                'nome_completo': paciente.nome_completo,
                'cpf': paciente.cpf,
                'data_nascimento': str(paciente.data_nascimento), # Converte DateField para string
                'celular': paciente.celular
            })
        return JsonResponse(pacientes_data, safe=False) # safe=False para listas

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            paciente = Paciente.objects.create(
                nome_completo=data['nome_completo'],
                cpf=data['cpf'],
                data_nascimento=data['data_nascimento'],
                celular=data['celular']
            )
            return JsonResponse({'mensagem': 'Paciente cadastrado com sucesso!', 'id': paciente.id}, status=201) # 201 Created
        except KeyError as e:
            return JsonResponse({'erro': f'Campo obrigatório faltando: {e}'}, status=400) # 400 Bad Request
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Corpo da requisição JSON inválido.'}, status=400)
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405) # 405 Method Not Allowed

@csrf_exempt
def paciente_detail_update_delete(request, id):
    """
    Detalha (GET), atualiza (PUT) ou remove (DELETE) um paciente específico.
    """
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'GET':
        # Serializa o objeto paciente para JSON
        paciente_data = {
            'id': paciente.id,
            'nome_completo': paciente.nome_completo,
            'cpf': paciente.cpf,
            'data_nascimento': str(paciente.data_nascimento),
            'celular': paciente.celular
        }
        return JsonResponse(paciente_data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # Atualiza apenas os campos fornecidos na requisição
            paciente.nome_completo = data.get('nome_completo', paciente.nome_completo)
            paciente.cpf = data.get('cpf', paciente.cpf)
            paciente.data_nascimento = data.get('data_nascimento', paciente.data_nascimento)
            paciente.celular = data.get('celular', paciente.celular)
            paciente.save()
            return JsonResponse({'mensagem': 'Paciente atualizado com sucesso!'})
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Corpo da requisição JSON inválido.'}, status=400)

    elif request.method == 'DELETE':
        paciente.delete()
        return JsonResponse({'mensagem': 'Paciente removido com sucesso!'})
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

# --- Funções para Agendamentos ---

@csrf_exempt
def agendamento_list_create(request):
    """
    Lista todas as consultas (GET) ou agenda uma nova consulta (POST).
    """
    if request.method == 'GET':
        agendamentos = Agendamento.objects.all()
        # Serializa a lista de agendamentos para JSON
        agendamentos_data = []
        for agendamento in agendamentos:
            agendamentos_data.append({
                'id': agendamento.id,
                'paciente_id': agendamento.paciente.id,
                'paciente_nome': agendamento.paciente.nome_completo,
                'data_hora': str(agendamento.data_hora), # Converte DateTimeField para string
                'tipo': agendamento.tipo,
                'especialidade': agendamento.especialidade,
                'status': agendamento.status # Inclui o status
            })
        return JsonResponse(agendamentos_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            paciente = get_object_or_404(Paciente, id=data['paciente_id'])
            agendamento = Agendamento.objects.create(
                paciente=paciente,
                data_hora=data['data_hora'],
                tipo=data['tipo'],
                especialidade=data['especialidade'],
                status='Agendado' # Define o status inicial como Agendado
            )
            return JsonResponse({'mensagem': 'Agendamento realizado com sucesso!', 'id': agendamento.id}, status=201)
        except KeyError as e:
            return JsonResponse({'erro': f'Campo obrigatório faltando: {e}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Corpo da requisição JSON inválido.'}, status=400)
        except Paciente.DoesNotExist:
            return JsonResponse({'erro': 'Paciente não encontrado.'}, status=404) # 404 Not Found

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def cancelar_agendamento(request, id):
    """
    Cancela uma consulta específica (PUT).
    """
    agendamento = get_object_or_404(Agendamento, id=id)

    if request.method == 'PUT':
        # Atualiza o status do agendamento para 'Cancelado'
        agendamento.status = 'Cancelado'
        agendamento.save()
        return JsonResponse({'mensagem': 'Agendamento cancelado com sucesso!'})
    
    return JsonResponse({'erro': 'Método não permitido'}, status=405)