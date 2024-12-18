from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Tour, Booking, Rating
from .forms import TourForm, BookingForm, OperatorLoginForm, RatingForm

# Главная страница: список всех туров
def home(request):
    tours = Tour.objects.all()
    for tour in tours:
        tour.rating_form = RatingForm()  # добавьте форму рейтинга для каждой тура
    return render(request, 'home.html', {'tours': tours})

# Страница "О нас"
def about_us(request):
    return render(request, 'tours/about_us.html')

# Страница "О Кыргызстане"
def kg(request):
    return render(request, 'tours/kg.html')

# Создание нового тура
@login_required
def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.operator = request.user
            tour.save()
            return redirect('operator_page')
    else:
        form = TourForm()
    return render(request, 'tours/create_tour.html', {'form': form})

# Страница туроператора
@login_required
def operator_page(request):
    tours = Tour.objects.filter(operator=request.user)
    bookings = Booking.objects.filter(tour__operator=request.user)
    return render(request, 'tours/operator_page.html', {'tours': tours, 'bookings': bookings})

# Бронирование тура
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        rating_form = RatingForm(request.POST)
        if booking_form.is_valid() and rating_form.is_valid():
            # Сохранение бронирования
            booking = booking_form.save(commit=False)
            booking.tour = tour
            booking.operator = tour.operator
            booking.save()

            # Сохранение оценки
            rating = rating_form.save(commit=False)
            rating.tour = tour
            rating.user = request.user
            rating.save()

            # Обновление среднего рейтинга
            tour_ratings = Rating.objects.filter(tour=tour)
            if tour_ratings.exists():
                average_rating = sum([rating.score for rating in tour_ratings]) / tour_ratings.count()
                tour.average_rating = average_rating
            else:
                tour.average_rating = 0.0  # или другое значение по умолчанию
            tour.save()

            return redirect('home')
    else:
        # Инициализация формы
        booking_form = BookingForm(initial={'tour': tour.id})
        rating_form = RatingForm()

    return render(request, 'tours/book_tour.html', {'booking_form': booking_form, 'rating_form': rating_form, 'tour': tour})

# Вход для туроператора
def operator_login(request):
    if request.method == 'POST':
        form = OperatorLoginForm(request.POST)
        if form.is_valid():
            user = form.user  # Здесь должно быть доступно поле 'user' после вызова метода 'clean'
            login(request, user)
            return redirect('operator_page')  # Перенаправление на нужную страницу
    else:
        form = OperatorLoginForm()

    return render(request, 'tours/operator_login.html', {'form': form})
