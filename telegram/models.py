from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import jwt

# Create your models here.


class BaseModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    class Meta:
        abstract = True


class PersonalUser(AbstractUser):
    token = models.CharField(
        max_length=256,
        verbose_name='ключ доступа',
        blank=True
    )
    telegram_id = models.IntegerField(
        verbose_name='telegram id',
        blank=True,
        null=True
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.username}'

    def generate_key(self):
        self.token = jwt.encode({'user_id': self.pk}, 'super_secret_key', algorithm='HS256').decode("utf-8")
    

class Message(BaseModel):
    user = models.ForeignKey(
        to=PersonalUser,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='пользователь'
    )
    body = models.TextField(
        verbose_name='тело сообщения'
    )
    status = models.BooleanField(
        verbose_name='отправлено',
        default=False
    )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
    
    def __str__(self):
        return self.body
    
    def info(self):
        return f'{self.body} {self.created}'