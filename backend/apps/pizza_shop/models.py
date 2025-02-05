from django.db import models
from core.models import BaseModel

class PizzaShopModel(BaseModel):
    class Meta:
        db_table = 'pizza_shops'

    name = models.CharField(max_length=25)
