from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from courses.models import Course, Lesson

NULLABLE = {"null": True, "blank": True}  # Необязательное поле


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Адрес электронной почты"
    )
    phone = models.CharField(
        max_length=35,
        **NULLABLE,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=100, **NULLABLE, verbose_name="Город", help_text="Укажите ваш город"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:  # Метаданные
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, **NULLABLE, related_name="payments"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, **NULLABLE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Оплата {self.amount} пользователем {self.user}"

    # user: Ссылка на модель пользователя (settings.AUTH_USER_MODEL). Указывает, кто совершил платеж.
    # payment_date: Дата и время оплаты. Устанавливается автоматически при создании записи.
    # course: Ссылка на оплаченный курс. Если пользователь платит за курс, это поле будет заполнено.
    #       Параметры NULLABLE означают, что оно не обязательно для заполнения.
    # lesson: Ссылка на оплаченный урок. Если платят за конкретный урок, это поле будет заполнено.
    #       Оно тоже необязательно.
    # amount: Сумма платежа с максимальным значением в 10 цифр и 2 знака после запятой.
    # payment_method: Способ оплаты, может быть либо "наличные", либо "перевод на счет".
    #       Для этого используется выбор из списка PAYMENT_METHOD_CHOICES