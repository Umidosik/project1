from .models import Tour, Booking, CustomUser

# Регистрируем модель CustomUser для админки
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_operator', 'is_staff', 'date_joined')
    list_filter = ('is_operator', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Поля для пользователя
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),  # Личные данные пользователя
        ('Права доступа', {'fields': ('is_operator', 'is_staff', 'is_active')}),  # Флаги доступа
        ('Даты', {'fields': ('last_login', 'date_joined')}),  # Даты регистрации и последнего входа
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_operator', 'is_staff', 'is_active')}),  # Права по умолчанию
    )

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)

# Регистрируем модель Tour
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'start_date', 'end_date', 'operator')
    search_fields = ('name', 'operator__username')  # Связываем оператор с туром
    list_filter = ('start_date', 'end_date')  # Фильтры по датам
exclude = ('average_rating',)  # Скрыть поле average_rating в админке

# Регистрируем модель Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone_number', 'email', 'tour', 'operator')  # Используем атрибут объекта, а не username
    search_fields = ('user_name', 'tour__name', 'operator__username')  # Поиск по имени пользователя, названию тура и имени оператора
    list_filter = ('tour',)  # Фильтр по туру


