from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# Create your views here.

def signup_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:list')
    else:
        form=UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method == "POST":
        print(f'--DEBUG submit button pressed')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(f'--DEBUG form is valid')
            print(f'--DEBUG user is {form.get_user()}')
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('movies:list')
    else:
        print(f'--DEBUG button not pressed')
        form=AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('movies:list')