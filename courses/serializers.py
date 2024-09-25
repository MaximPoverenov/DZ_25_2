from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from courses.models import Course, Lesson, CourseSubscription
from courses.validators import YouTubeValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "video_url"]
        validators = [
            YouTubeValidator(field="video_url")
        ]  # Валидатор для проверки ссылки на видео


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()  # Счетчик уроков

    # Поле для вывода информации обо всех уроках
    # many=True - указываем, что мы хотим получить список уроков
    lessons = LessonSerializer(many=True, read_only=True)

    # Метод для подсчета уроков
    def get_lessons_count(self, obj):
        return obj.lessons.count()  # Подсчет количества связанных уроков

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]  # Указываем новое поле в fields

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return CourseSubscription.objects.filter(user=user, course=obj).exists()
        return False


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = ["user", "course", "subscribed_at"]