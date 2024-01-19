from django.db import models
from django.contrib.auth.models import AbstractUser


class UserCustom(AbstractUser):
    """
    Modelo personalizado que estende o AbstractUser do Django

    Atribui um campo email como identifcador único na autenticação

    O objetivo é fazer com que os usuários assim como o superusuário utilizem
    o email como forma de login, ao invés de usar o username

    Para isso, foi utilizado a variável estática USERNAME_FIELD = 'email'.
    A partir dessa atribuição, todos que queiram logar no site, terão que usar
    o email como autenticador principal
    """

    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
