from django import forms


class LoginForm(forms.Form):
    # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
    username = forms.CharField(label='', required=True)
    password = forms.CharField(label='', required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='', required=True, min_length=6)

