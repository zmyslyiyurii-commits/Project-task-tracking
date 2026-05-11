from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task, Project

def main(request):
    return render(request, 'main.html')

def logout_view(request):
    auth_logout(request) 
    return redirect('main')

# Домашня сторінка
@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tasks': tasks,
        'projects': projects,
    }
    return render(request, 'home.html', context)

@login_required
def create_item(request):
    if request.method == 'POST':
        try:
            mode = request.POST.get('mode')
            title = request.POST.get('title')
            desc = request.POST.get('description', '')
            p_id = request.POST.get('project_id')

            if not title or title.strip() == "":
                return JsonResponse({'status': 'error', 'message': 'Назва не може бути порожньою'}, status=400)

            if mode == 'project':
                Project.objects.create(name=title, description=desc, user=request.user)
            else:
                proj = None
                if p_id and p_id.isdigit():
                    proj = Project.objects.filter(id=p_id, user=request.user).first()
                
                Task.objects.create(title=title, description=desc, project=proj, user=request.user)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Це поверне реальний текст помилки в JS alert
            return JsonResponse({'status': 'error', 'message': f"Помилка бази: {str(e)}"}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не дозволено'}, status=405)
# Вхід у систему
def login_view(request):
    if request.method == "POST":
        u_login = request.POST.get('username') 
        u_pass = request.POST.get('password')
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
            if User.objects.filter(username=u_name).exists():
                messages.error(request, "Користувач з таким ім'ям вже існує")
            else:
                user = User.objects.create_user(username=u_name, email=u_email, password=u_pass)
                auth_login(request, user) 
                return redirect("home") 
            
    return render(request, "registers/register.html")