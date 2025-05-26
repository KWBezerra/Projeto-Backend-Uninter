
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password,check_password
import json
import uuid
from .models import Funcionario


@csrf_exempt
def cadastrar_funcionario(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        dados = json.loads(request.body)

        nome = dados.get('nome')
        data_nascimento = dados.get('data_nascimento')
        matricula = dados.get('matricula')
        senha = dados.get('senha')

        if not all([nome, data_nascimento, matricula, senha]):
            return JsonResponse({'erro': 'Todos os campos são obrigatórios'}, status=400)

        if Funcionario.objects.filter(matricula=matricula).exists():
            return JsonResponse({'erro': 'Matrícula já cadastrada'}, status=400)

        funcionario = Funcionario.objects.create(
            nome=nome,
            data_nascimento=parse_date(data_nascimento),
            matricula=matricula,
            senha=make_password(senha)
        )

        return JsonResponse({'mensagem': 'Funcionário cadastrado com sucesso'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)


@csrf_exempt
def login_funcionario(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        dados = json.loads(request.body)
        matricula = dados.get('matricula')
        senha = dados.get('senha')

        if not matricula or not senha:
            return JsonResponse({'erro': 'Matrícula e senha são obrigatórias'}, status=400)

        try:
            funcionario = Funcionario.objects.get(matricula=matricula)
        except Funcionario.DoesNotExist:
            return JsonResponse({'erro': 'Funcionário não encontrado'}, status=404)

        if check_password(senha, funcionario.senha):
            token = str(uuid.uuid4())
            funcionario.token = token
            funcionario.save()
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'erro': 'Senha incorreta'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    
@csrf_exempt
def logout_funcionario(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        dados = json.loads(request.body)
        token = dados.get('token')

        if not token:
            return JsonResponse({'erro': 'Token é obrigatório'}, status=400)

        try:
            funcionario = Funcionario.objects.get(token=token)
        except Funcionario.DoesNotExist:
            return JsonResponse({'erro': 'Token inválido'}, status=401)

        funcionario.token = None
        funcionario.save()
        return JsonResponse({'mensagem': 'Logout realizado com sucesso'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)