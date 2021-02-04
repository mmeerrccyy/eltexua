from django import forms
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата отримання замовлення'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'order_date',
            'comment'
        )


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Неправильний логін або пароль!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неправильний логін або пароль!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['phone'].label = 'Номер телефону'
        self.fields['email'].label = 'Елетронна пошта'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Підтвердити пароль'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Ім\'я {username} вже зайняте')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username',
            'phone',
            'email',
            'password',
            'confirm_password'
        ]
