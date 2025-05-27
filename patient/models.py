from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    celular = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_completo

class Agendamento(models.Model):
    TIPO_CHOICES = (
        ('consulta', 'Consulta'),
        ('exame', 'Exame'),
    )
    STATUS_CHOICES = [ # Adicionado para o campo status
        ('Agendado', 'Agendado'),
        ('Cancelado', 'Cancelado'),
        ('Concluido', 'Concluído'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    especialidade = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Agendado') # Novo campo status

    def __str__(self):
        return f'{self.tipo.title()} de {self.paciente.nome_completo} em {self.data_hora.strftime("%d/%m/%Y %H:%M")}'

