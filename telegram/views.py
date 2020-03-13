from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

# Create your views here.

from .forms import CustomRegisterForm, CustomAuthForm


def index(request):
    return render(request, 'index.html')


class MyRegisterFormView(FormView):
    form_class = CustomRegisterForm
    success_url = '/login/'
    template_name = 'account/register.html'

    def form_valid(self, form):
        form.save()
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


class MyLoginFormView(LoginView):
    form_class = CustomAuthForm
    success_url = '/'
    template_name = 'account/login.html'


class MyLogoutFormView(LogoutView):
    next_page = '/'