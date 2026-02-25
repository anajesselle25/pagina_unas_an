from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Tu Nombre de Usuario', 'class': 'main__input'})
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder':'Tu Contraseña', 'class': 'main__input'})
    )