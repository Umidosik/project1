from django.db import models
from django.contrib.auth.models import AbstractUser

# Кастомная модель пользователя
class CustomUser(AbstractUser):
    is_operator = models.BooleanField(default=False)

# Модель тура
class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    operator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    route = models.TextField(help_text="Маршрут тура", blank=True, null=True)
    included = models.TextField(help_text="Что включено в тур", blank=True, null=True)
    not_included = models.TextField(help_text="Что не включено в тур", blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='default.jpg')
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0  # Значение по умолчанию
    )

    def __str__(self):
        return self.name

# Модель бронирования
class Booking(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    tour = models.ForeignKey(Tour, related_name='bookings', on_delete=models.CASCADE)
    operator = models.ForeignKey(CustomUser, related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Заявка от {self.user_name} на тур {self.tour.name}"

from django.db import models
from django.conf import settings

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(null=True, blank=True)  # Позволяет оставлять поле пустым

    def __str__(self):
        return f"Rating {self.score} for tour {self.tour.name} by {self.user.username}"
