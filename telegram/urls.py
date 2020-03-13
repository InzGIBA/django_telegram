from django.urls import path

# Create your urls here.

from .views import MyRegisterFormView, MyLoginFormView, MyLogoutFormView, index

urlpatterns = [
    path('', index, name='index'),
    path('register/', MyRegisterFormView.as_view(), name='account.register'),
    path('login/', MyLoginFormView.as_view(), name='account.login'),
    path('logout/', MyLogoutFormView.as_view(), name='account.logout'),
]
