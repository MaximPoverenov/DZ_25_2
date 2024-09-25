from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payment
from users.serializers import UsersSerializer, PaymentSerializer, RegisterSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Доступ только для авторизованных пользователей


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Определяем фильтры для полей
    filterset_fields = ["course", "lesson", "payment_method"]

    # Поле для сортировки
    ordering_fields = ["payment_date"]

    # По умолчанию сортировать по дате оплаты
    ordering = ["payment_date"]


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)