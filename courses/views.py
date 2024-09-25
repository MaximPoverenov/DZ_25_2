from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from courses.models import Course, Lesson, CourseSubscription
from courses.paginators import CourseLessonPagination
from courses.permissions import IsOwnerOrReadOnly
from courses.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем курс к пользователю

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            # Запрещаем модераторам создавать и удалять курсы
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            # Модераторам разрешено только изменение курсов
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            # Разрешаем чтение любым аутентифицированным пользователям
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # Для уроков

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем урок к пользователю

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ к объекту только владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Все могут читать (GET), но только владелец может изменять (PUT, PATCH, DELETE)
        if request.method in ("GET",):
            return True
        return (
            obj.owner == request.user
        )  # Проверка, что пользователь — владелец объекта


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем курс к пользователю


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем урок к пользователю


class CourseSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subscription = CourseSubscription.objects.filter(user=user, course=course_item)

        if subscription.exists():
            # Если подписка существует — удаляем
            subscription.delete()
            message = "Подписка удалена"
        else:
            # Если подписки нет — создаем
            CourseSubscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination