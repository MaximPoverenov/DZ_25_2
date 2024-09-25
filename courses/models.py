from django.conf import settings
from django.db import models

from courses.validators import validate_youtube_link

NULLABLE = {"null": True, "blank": True}  # Необязательное поле


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        related_name="courses",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        **NULLABLE,
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание курса", help_text="Укажите описание курса"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="lessons",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Название лекции",
        help_text="Укажите название лекции",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание лекции", help_text="Укажите описание лекции"
    )
    preview = models.ImageField(
        upload_to="lesson_previews/",
        **NULLABLE,
        verbose_name="Превью лекции",
        help_text="Загрузите превью лекции",
    )
    video_url = models.URLField(
        validators=[validate_youtube_link],
        **NULLABLE,
        verbose_name="Видео",
        help_text="Укажите видео",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} подписан на {self.course.title}"