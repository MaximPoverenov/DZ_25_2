from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "courses/", include("courses.urls", namespace="courses")
    ),  # Подключаем отдельные маршруты для курсов
    path(
        "users/", include("users.urls", namespace="users")
    ),  # Подключаем отдельные маршруты для пользователей
]