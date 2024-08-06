from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Genre,Movies,Reviews
from .forms import genreforms,Moviesforms,MovieStatusForm
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
            return redirect('genreList')
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
            return redirect('genreList')
    else:
        form = genreforms(instance=genres)
    return render(request,'genre/editgenre.html',{'form':form})

@login_required(login_url='/')
def Deletegenre(request,genre_id):
    genres = Genre.objects.get(id=genre_id)
    if request.method == "POST":
        genres.delete()
        messages.success(request, 'Genres Successfully Deleted!')
        return redirect('genreList')


@login_required(login_url='/')
def listmovies(request):
    movies = Movies.objects.all()
    return render(request,'movie/movieslist.html',{'movies':movies})

@login_required(login_url='/')
def createmovies(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['users'] = request.user.id
        post_data['approval_status'] = 1
        form = Moviesforms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movieslist')
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


def update_movie_status(request,pk,status):
    movie = get_object_or_404(Movies,pk=pk)
    movie.approval_status = status
    movie.save()
    return redirect('movieslist')

@login_required(login_url='/')
def Deletemovies(request,movie_id):
    movies = Movies.objects.get(id=movie_id)
    if request.method == "POST":
        movies.delete()
        messages.success(request, 'Movies Successfully Deleted!')
        return redirect('movieslist')

def Listreviews(request):
    reviews = Reviews.objects.all()
    return render(request, 'movie/reviewslist.html', {'reviews': reviews})

def Updatecommentstatus(request,pk,status):
    review = get_object_or_404(Reviews,pk=pk)
    review.active=status
    review.save()
    return redirect('Reviewslist')







