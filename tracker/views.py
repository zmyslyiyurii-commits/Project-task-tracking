from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def main(request):
    return render(request, 'main.html')

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        # Змінюємо 'email' на 'username', бо зазвичай в HTML саме так підписано поле
        u_login = request.POST.get('username') 
        u_pass = request.POST.get('password')
        
        # Якщо ти ТОЧНО впевнений, що в HTML формі <input name="email">, 
        # тоді залиш email, але зазвичай Django-юзери логіняться через username.
        
        user = authenticate(request, username=u_login, password=u_pass)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Невірний логін або пароль")
    
    return render(request, "registers/login.html")

def register_view(request):
    if request.method == "POST":
        
        u_name = request.POST.get('username')
        u_email = request.POST.get('email')
        u_pass = request.POST.get('password')

        if u_name and u_pass:
            user = User.objects.create_user(username=u_name, email=u_email, password=u_pass)
            auth_login(request, user) 
            return redirect("home") 
            
    return render(request, "registers/register.html")