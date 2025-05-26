from django.db import models
from patient.models import Agendamento  
from register.models import Funcionario

class Prontuario(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='prontuario')
    paciente_nome = models.CharField(max_length=255)
    idade = models.IntegerField()
    data_consulta = models.DateField()
    
    queixa_principal = models.TextField()
    historia_clinica = models.TextField()
    
    antecedentes = models.TextField(blank=True, null=True)
    medicacoes = models.TextField(blank=True, null=True)
    
    pa = models.CharField("Pressão Arterial", max_length=20, blank=True, null=True)
    fc = models.CharField("Frequência Cardíaca", max_length=20, blank=True, null=True)
    ausculta = models.TextField(blank=True, null=True)

    impressao_diagnostica = models.TextField()
    conduta = models.TextField()

    medico_nome = models.CharField(max_length=255)
    medico_crm = models.CharField(max_length=50)
    
    criado_por = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prontuário - {self.paciente_nome} ({self.data_consulta})"
