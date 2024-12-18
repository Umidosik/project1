from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница с турами
    path('tour/<int:tour_id>/book/', views.book_tour, name='book_tour'),  # Страница бронирования тура
    path('operator/', views.operator_page, name='operator_page'),  # Страница туроператора
    path('operator/login/', views.operator_login, name='operator_login'),  # Страница входа для туроператора
    path('create/', views.create_tour, name='create_tour'),  # Страница создания тура
    path('about_us/', views.about_us, name='about_us'),  # Страница "О нас"
    path('kg/', views.kg, name='kg'),  # Страница "О Кыргызстане"
    path('book_tour/<int:tour_id>/', views.book_tour, name='book_tour'),  # Детальная информация о туре
]
