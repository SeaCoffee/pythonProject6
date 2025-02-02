from django.db import models

class PizzaQuerySet(models.QuerySet):
    def less_size(self, size):
        return self.filter(size_lt=size)



class PizzaManager(models.Manager):
    def get_queryset(self):
        return PizzaQuerySet(self.model)

    def less_seize(self, size):
        return self.get_queryset().less_size(size)