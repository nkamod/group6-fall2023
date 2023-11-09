from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


def connectInsta(request):
    print(request.body)
    return JsonResponse({"status": "success"})


def delete_account(user=None):
    if user is not None:
        user.delete()
    else:
        raise User.DoesNotExist


@login_required
def profile(request, user_name):
    # For now, the only POST request is used to delete account.
    # In the future, this must be checked further to very what the user want. (ex: delete vs. manage metrics
    if request.method == "POST":
        user_to_delete = request.user
        delete_account(user_to_delete)
        return redirect('popularity_assessor:login')
    return render(request, 'profile.html', {"count": [1, 2, 3]})


def register(request):
    # Handle the POST request (form submission)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after registration and redirect to profile
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('popularity_assessor:profile',
                            user_name=new_user.username)
    # Handle the GET request (displaying the form)
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('popularity_assessor:profile',
                            user_name=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
