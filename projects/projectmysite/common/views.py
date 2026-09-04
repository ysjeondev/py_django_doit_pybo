from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserForm


def signup(request):
    # 회원가입 버튼을 눌렀을 때
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(
                username=username,
                password=raw_password
            )

            login(request, user)

            return redirect('index')

    # 주소창으로 회원가입 화면에 들어왔을 때
    else:
        form = UserForm()

    context = {
        'form': form
    }

    return render(
        request,
        'common/signup.html',
        context
    )