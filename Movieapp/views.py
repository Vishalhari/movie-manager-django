from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Genre,Movies
from .forms import genreforms,Moviesforms
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def Genrelist(request):
    genres = Genre.objects.all()
    return render(request,'genre/genrelist.html',{'genres':genres})

@login_required(login_url='/')
def Creategenre(requests):
    if requests.method == "POST":
        form = genreforms(requests.POST)
        if form.is_valid():
            form.save()
            messages.success(requests, 'Genre Added Successfully!')
            return redirect('genrelist')
    else:
     form = genreforms()
    return render(requests,'genre/creategenre.html',{'form':form})

@login_required(login_url='/')
def Editgenre(request,genre_id):
    genres = Genre.objects.get(id=genre_id)
    if request.method == "POST":
        form = genreforms(request.POST,instance=genres)

        if form.is_valid():
            form.save()
            messages.success(request, 'Genre Successfully Updated!')
            return redirect('genrelist')
    else:
        form = genreforms(instance=genres)
    return render(request,'genre/editgenre.html',{'form':form})

@login_required(login_url='/')
def Deletegenre(request,genre_id):
    genres = Genre.objects.get(id=genre_id)
    if request.method == "POST":
        genres.delete()
        messages.success(request, 'Genres Successfully Deleted!')
        return redirect('genrelist')


@login_required(login_url='/')
def listmovies(request):
    movies = Movies.objects.all()
    return render(request,'movie/movieslist.html',{'movies':movies})

@login_required(login_url='/')
def createmovies(request):
    if request.method == 'POST':
        form = Moviesforms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Moviesforms()
    return render(request,'movie/createmovies.html',{'form':form})

@login_required(login_url='/')
def Editmovies(request,movie_id):
    movies = Movies.objects.get(id=movie_id)
    if request.method == 'POST':
        form = Moviesforms(request.POST,instance=movies)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movies Successfully Updated!')
            return redirect('movieslist')
    else:
        form = Moviesforms(instance=movies)
    return render(request, 'movie/Editmovies.html', {'form': form,'movie':movies})

@login_required(login_url='/')
def Deletemovies(request,movie_id):
    movies = Movies.objects.get(id=movie_id)
    if request.method == "POST":
        movies.delete()
        messages.success(request, 'Movies Successfully Deleted!')
        return redirect('movieslist')






