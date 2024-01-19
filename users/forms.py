from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserCustom
from django.forms import ValidationError
from django.contrib.auth.forms import PasswordResetForm


class UserForm(UserCreationForm):
    """
        Classe que fornecerá a classe UserForm o modelo a qual deve ser seguido.
        Neste código, o model que está sendo passado é o UserCustom, ou seja,
        os campos contidos em UserCustom podem ser acessados pela classe UserForm.

        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

        O atributo acima informa quais campos da classe UserCustom devem ser acessados pela
        classe UserForm
    """

    class Meta:

        model = UserCustom
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if UserCustom.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'o nome de usuário {self.username} já está em uso')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if UserCustom.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Email {self.email} já está em uso')
        return email


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Seu Email'}))

