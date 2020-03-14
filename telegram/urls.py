from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your urls here.

from .views import MyRegisterFormView, MyLoginFormView, MyLogoutFormView
from .views import index, token
from .views import MessageListView, MessageCreateView
from .views import MessageView
from .bots import BotView


urlpatterns = [
    path('', index, name='index'),
]

accountpatterns = [
    path('accounts/token/', token, name='account.token'),
    path('accounts/register/', MyRegisterFormView.as_view(), name='account.register'),
    path('accounts/login/', MyLoginFormView.as_view(), name='account.login'),
    path('accounts/logout/', MyLogoutFormView.as_view(), name='account.logout'),
]

messagepatterns = [
    path('messages/', MessageListView.as_view(), name='message.list'),
    path('message/create', MessageCreateView.as_view(), name='message.create'),
]

telegrampatterns = [
    path('bot/', BotView.as_view(), name='telegram.bot'),
    path('1098645129:AAHysl9Eq2SHm6Hrj_oAX2ZGuyXcsNmtZyg/', BotView.as_view(), name='telegram.webhook'),
]

apipatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/messages/', MessageView.as_view(), name='api.message'),
]

urlpatterns += accountpatterns
urlpatterns += messagepatterns
urlpatterns += telegrampatterns
urlpatterns += apipatterns
