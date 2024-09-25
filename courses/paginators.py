from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    # Количество элементов на странице
    page_size = 10

    # Параметр запроса для изменения количества элементов на странице
    page_size_query_param = "page_size"

    # Максимальное количество элементов на странице
    max_page_size = 100