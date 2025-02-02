from django_filters import rest_framework as filters
from apps.pizza.models import DaysChoices, PizzaModel

class PizzaFilter(filters.FilterSet):
    lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    range = filters.RangeFilter(field_name='size')  # range_min=2&range_max=100
    price_in = filters.BaseInFilter(field_name='price')  # price_in=30,25,2000
    day = filters.ChoiceFilter('day', choices=DaysChoices.choices)
    order = filters.OrderingFilter(
        fields={
            'id',
            'name',
            'price',
        }
    )  # order=name.asc

