from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, AddMovieForm, UpdateMovieForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from .models import Movie

from django.contrib import messages


# home
def home(request):
    return render(request, 'movieapp/index.html')


# register

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("my_login")

    else:
        form = CreateUserForm()
    return render(request, 'movieapp/register.html', {'form': form})


# login_user

def my_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'movieapp/my_login.html', {'form': form})


@login_required(login_url='my_login')
def dashboard(request):
    movies = Movie.objects.all()

    context = {'movie': movies}

    return render(request, 'movieapp/dashboard.html', context=context)


@login_required(login_url='my_login')
def add_movie(request):
    form = AddMovieForm()

    if request.method == "POST":

        form = AddMovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = form.save(commit=False)

            movie.user = request.user

            form.save()

            messages.success(request, "Your movie is added!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'movieapp/add_movie.html', context=context)


@login_required(login_url='my_login')
def detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'movieapp/detail.html', {'movie': movie})


@login_required(login_url='my_login')
def update(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.user != request.user:
        return HttpResponseForbidden("")

    if request.method == 'POST':
        form = UpdateMovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = UpdateMovieForm(instance=movie)

        return render(request, 'movieapp/edit.html', {'form': form, 'movie': movie})


@login_required(login_url='my_login')
def delete(request, id):
    movie = get_object_or_404(Movie, id=id)

    if movie.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this movie.")

    if request.method == 'POST':
        movie.delete()
        return redirect("dashboard")
    return render(request, 'movieapp/delete.html')


# - User logout

def user_logout(request):
    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("my_login")
