from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


UserModel = get_user_model()
class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")  # Поиск по email (регистронезависимый)
    is_active = filters.BooleanFilter(field_name="is_active")  # Фильтр по активности
    is_staff = filters.BooleanFilter(field_name="is_staff")  # Фильтр по роли staff
    created_range = filters.DateFromToRangeFilter(field_name="created_at")  # Диапазон дат создания
    order = filters.OrderingFilter(fields=("id", "email", "created_at"))  # Сортировка

    class Meta:
        model = UserModel
        fields = ["email", "is_active", "is_staff", "created_at"]  # Доступные фильтры
