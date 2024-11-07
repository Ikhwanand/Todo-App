from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task 
from .forms import TaskForm, SignUpForm, LoginForm


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('todo_app:task_list')
    else:
        form = SignUpForm()
    return render(request, 'todo_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo_app:task_list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'todo_app/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('todo_app:login')



def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = []
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    return render(request, 'todo_app/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todo_app:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo_app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todo_app:task_list')
    return render(request, 'todo_app/task_confirm.html', {'task': task})