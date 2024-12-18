from django.contrib.auth import authenticate
from django import forms
from django.core.exceptions import ValidationError
from .models import Tour, Booking
from django import forms
from .models import Rating

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'description', 'price', 'start_date', 'end_date', 'operator', 'route', 'included', 'not_included', 'image']
        labels = {
            'name': 'Название тура',
            'description': 'Описание тура',
            'price': 'Цена',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'operator': 'Имя туроператора',
            'route': 'Маршрут тура',
            'included': 'Что включено в тур',
            'not_included': 'Что не включено в тур',
            'image': 'Изображение'
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_name', 'phone_number', 'email', 'tour']
        labels = {
            'user_name': 'Имя пользователя',
            'phone_number': 'Номер телефона',
            'email': 'Электронная почта',
            'tour': 'Выберите тур'
        }
        widgets = {
            'tour': forms.HiddenInput(),  # скрытое поле для тура
        }

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class OperatorLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Неверное имя пользователя или пароль.")
        if not getattr(user, 'is_operator', False):  # Проверяем, является ли пользователь туроператором
            raise ValidationError("У вас нет прав доступа как туроператор.")

        # Сохраняем пользователя для использования в представлении
        self.user = user
        return cleaned_data

class RatingForm(forms.ModelForm):
    class Meta:
            model = Rating
            fields = ['score']
            labels = {
                'score': 'Оценка'
            }
            widgets = {
                'score': forms.Select(choices=[(i, f'{i} звезда{"s" if i > 1 else ""}') for i in range(1, 6)])
            }
