from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as authlogin,logout as authlogout
from django.contrib.auth.decorators import login_required
from .forms import UsersForm
from Movieapp.models import Genre,Movies


def adminlogin(request):
    error_message = None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        admin = authenticate(username=username,password=password)

        if admin:
            authlogin(request,admin)
            return redirect('admindashboard')
        else:
            error_message = "invalid user"
    return render(request,'user/login.html',{'error_message':error_message})

@login_required(login_url='/')
def admindashboard(request):
    users = User.objects.filter(is_superuser=False).count()
    genres = Genre.objects.count()
    movies = Movies.objects.count()
    context = {
        'usercount':users,
        'genres':genres,
        'movies':movies
    }
    return render(request,'user/dashboard.html',context)

@login_required(login_url='/')
def Userslist(request):
    users = User.objects.filter(is_superuser=False)
    return render(request,'user/userslist.html',{'users':users})

@login_required(login_url='/')
def Editusers(request,user_id):
    users = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UsersForm(request.POST,instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Successfully Updated!')
            return redirect('userslist')
    else:
        form = UsersForm(instance=users)
    return render(request, 'user/editusers.html', {'form': form})


@login_required(login_url='/')
def Deleteusers(request,user_id):
    users = User.objects.get(id=user_id)
    if request.method == "POST":
        users.delete()
        messages.success(request, 'User Successfully Deleted!')
        return redirect('userslist')

@login_required(login_url='/')
def Createusers(request):
    user = None
    error_message = None
    if request.POST:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        mail = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_user(
                    first_name=firstname,
                    last_name=lastname,
                    email=mail,
                    username=username,
                    password=password
                  )
            messages.success(request, 'User Added Successfully!')
            return redirect('userslist')
        except Exception as e:
            error_message = str(e)
    form = UsersForm()
    return render(request, 'user/createusers.html',{'form':form,'user':user,'error_message':error_message})


def Adminlogout(request):
    authlogout(request)
    return redirect('adminlogin')


