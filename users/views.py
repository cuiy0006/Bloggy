from django.shortcuts import render, redirect
from users.forms import RegisterFrom
# from users.forms import PwdChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
def register(request):

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = RegisterFrom(request.POST)

        if form.is_valid():
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterFrom()
    return render(request, 'users/register.html', context={'form':form, 'next':redirect_to})

def password_change(request):

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            #messages.success(request, 'Your password was successfully updated!')

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
        else:
            pass
            #messages.error(request, "Please correct error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', context={'form': form, 'next':redirect_to})
