from django.db import models
from django.core import validators as V

from core.models import BaseModel
from apps.pizza_shop.models import PizzaShopModel
from core.enums.regex_enum import RegexEnum
from apps.pizza.managers import PizzaManager
from core.services.file_service import upload_pizza_photo

class DaysChoices(models.TextChoices):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'

class PizzaModel(BaseModel):
    class Meta:
        db_table = 'pizzas'
    name = models.CharField(max_length=25, validators=[V.RegexValidator(RegexEnum.NAME.pattern, RegexEnum.NAME.msg)])
    price = models.IntegerField(validators=[V.MinValueValidator(1), V.MaxValueValidator(100)])
    size = models.IntegerField()
    day = models.CharField(max_length=10, choices=DaysChoices.choices)
    pizza_shop = models.ForeignKey(PizzaShopModel, on_delete=models.CASCADE, related_name='pizzas')
    photo = models.ImageField(upload_to=upload_pizza_photo, blank=True)

    objects = PizzaManager()