# Clínica Back-End API

API desenvolvida em Django para gerenciamento de uma clínica médica. Este sistema contempla o cadastro de funcionários e pacientes, agendamento de consultas, e controle de prontuários médicos.

## ▶️ Como executar

```bash
git clone https://github.com/KWBezerra/Projeto-Backend-Uninter
cd seu-repositorio
python -m venv venv
source venv/bin/activate | ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🚀 Funcionalidades

- Cadastro de funcionários
- Cadastro de pacientes
- Agendamento e cancelamento de consultas/exames
- Criação e edição de prontuários médicos
- Consulta de prontuário por agendamento
- Histórico de consultas do paciente

## 🛠️ Tecnologias

- Python 3.13.3
- Django 5.2.1
- SQLite (pode ser trocado por PostgreSQL)

## 📁 Estrutura

- `register/`: Cadastro de pacientes e funcionários / Login de funcionarios e pacientes(Futuro).
- `patient/`: gerenciamento de consultas e pacientes.
- `controll/`: Prontuários médicos.

## 🔒 Segurança

Utiliza autenticação do Django e proteção CSRF. O sistema segue os padrões do Django para prevenção de falhas como:
- Injeção SQL
- CSRF (Cross-Site Request Forgery)
- XSS (Cross-Site Scripting)


