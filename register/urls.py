from django.urls import path
from .views import cadastrar_funcionario, login_funcionario, logout_funcionario

urlpatterns = [
    path('register/funcionario/', cadastrar_funcionario),
    path('login/', login_funcionario),
    path('logout/', logout_funcionario),
]
