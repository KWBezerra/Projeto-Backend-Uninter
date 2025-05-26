from django.contrib import admin
from .models import Paciente, Agendamento

# Register your models here.

admin.site.register(Paciente)
admin.site.register(Agendamento)