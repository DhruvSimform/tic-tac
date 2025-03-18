from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout

from django.contrib import messages

# Create your views here.
def login_page(request):
    next_page = request.GET.get('next', 'home')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(next_page)
        else:
            messages.error(request,'Incorrect username and password')
    return render(request,'account/login_page.html')


# Create your views here.
def register_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        user = User(username=username , email=email)
        user.set_password(password)
        user.save()
        messages.success(request,f"{username} , registration done.")
        return redirect('login-page')

    return render(request,'account/register_page.html')

def logout_page(request):
    logout(request)
    return redirect('home')