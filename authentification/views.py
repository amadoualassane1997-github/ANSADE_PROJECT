from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from authentification.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from authentification.decorators import unauthenticated_user
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='user')
            user.groups.add(group)
            messages.success(request,'Account was created for' +username)
            return redirect('login')

    context={'form':form}
    return render(request,'authentification/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('blog-home')
        else:
            messages.info(request,"Username or Password is incorrect")
        
    
    context={}
    return render(request,'authentification/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')
