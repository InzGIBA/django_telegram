# Simple render page
from django.shortcuts import render
# Support urls names
from django.urls import reverse_lazy
# Auth views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
# Auth decotators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Generic views
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
# API
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

from .forms import CustomRegisterForm, CustomAuthForm, CustomMessageForm
from .models import Message
from .serializers import MessageSerializer
from .bots import send_message


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        message = Message.objects.filter(user=user)
        serializer = MessageSerializer(message, many=True)
        return Response({"message": serializer.data})

    def post(self, request):
        message = request.data.get('message')
        serializer = MessageSerializer(data=message)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save(user=request.user)
            try:
                send_message(message_saved.user.telegram_id, f'{message_saved.user}, я получил от тебя сообщение:\n{message_saved.body}')
            except  Exception as e:
                print(e)
            else:
                message_saved.status = True
                message_saved.save()
        return Response({"success": "Message '{}' created successfully".format(message_saved.body)})


class MessageCreateView(CreateView):
    model = Message
    form_class = CustomMessageForm
    success_url = reverse_lazy('message.list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        try:
            if obj.user.telegram_id:
                send_message(obj.user.telegram_id, f'{obj.user}, я получил от тебя сообщение:\n{obj.body}')
        except Exception as e:
            print(e)
        else:
            obj.status = True
        return super(MessageCreateView, self).form_valid(form)


class MessageListView(ListView):
    model = Message

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MessageListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(MessageListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MyRegisterFormView(FormView):
    form_class = CustomRegisterForm
    success_url = reverse_lazy('account.login')
    template_name = 'account/register.html'

    def form_valid(self, form):
        form.save()
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


class MyLoginFormView(LoginView):
    form_class = CustomAuthForm
    success_url = reverse_lazy('index')
    template_name = 'account/login.html'


class MyLogoutFormView(LogoutView):
    next_page = reverse_lazy('index')


def index(request):
    return render(request, 'index.html')


def token(request):
    return render(request, 'token.html')