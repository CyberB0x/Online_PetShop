from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

User = get_user_model()  # твой кастомный пользователь

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Проверки
        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Имя пользователя уже занято.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email уже используется.")
            return redirect("register")

        # Создаём пользователя
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Регистрация успешна! Добро пожаловать 🚀")
        return redirect("home")

    return render(request, "register.html")


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Добро пожаловать обратно!")
            return redirect("home")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("home")
