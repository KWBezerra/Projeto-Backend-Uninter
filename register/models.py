import uuid
from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    matricula = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)  # Armazenada com hash
    token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} ({self.matricula})'
