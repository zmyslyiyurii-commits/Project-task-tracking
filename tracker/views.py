from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task, Project, UserActivity
import json
from datetime import timedelta
from django.utils import timezone

def main(request):
    return render(request, 'main.html')

def logout_view(request):
    auth_logout(request) 
    return redirect('main')

@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user, is_completed=False).order_by('-created_at') 
    projects = Project.objects.filter(user=request.user).order_by('-created_at') 
    today = timezone.now().date() 
    last_week = today - timedelta(days=6) 
    activities = UserActivity.objects.filter(user=request.user, date__gte=last_week).order_by('date') 
    activity_data = {(last_week + timedelta(days=i)).isoformat(): 0 for i in range(7)}
    for a in activities:
        activity_data[str(a.date)] = a.seconds_spent // 60 
    
    context = {
        'tasks': tasks, 
        'projects': projects, 
        'activity_json': json.dumps(activity_data), 
    }
    return render(request, 'home.html', context) 

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.save()
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project.delete()
    return redirect('home')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project_tasks = Task.objects.filter(project=project).order_by('is_completed', '-created_at')
    return render(request, 'project_detail.html', {'project': project, 'project_tasks': project_tasks})

@login_required
def create_item(request):
    if request.method == 'POST':
        try:
            mode = request.POST.get('mode')
            title = request.POST.get('title')
            desc = request.POST.get('description', '')
            p_id = request.POST.get('project_id')
            if not title or title.strip() == "":
                return JsonResponse({'status': 'error', 'message': 'Назва порожня'}, status=400)
            if mode == 'project':
                Project.objects.create(name=title, description=desc, user=request.user)
            else:
                proj = Project.objects.filter(id=p_id, user=request.user).first() if p_id else None
                Task.objects.create(title=title, description=desc, project=proj, user=request.user)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)

def login_view(request):
    if request.method == "POST":
        u_login, u_pass = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=u_login, password=u_pass)
        if user:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, "Невірний логін або пароль")
    return render(request, "registers/login.html")

def register_view(request):
    if request.method == "POST":
        u_name, u_email, u_pass = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        if u_name and u_pass:
            if User.objects.filter(username=u_name).exists():
                messages.error(request, "Користувач існує")
            else:
                user = User.objects.create_user(username=u_name, email=u_email, password=u_pass)
                auth_login(request, user)
                return redirect("home")
    return render(request, "registers/register.html")