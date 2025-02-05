from django.urls import path

from apps.pizza_shop.views import PizzaShopListCreateView, PizzaShopAddPizzaView


urlpatterns = [
   path('', PizzaShopListCreateView.as_view(), name='pizza_shops'),
   path('/<int:pk>/pizzas', PizzaShopAddPizzaView.as_view(), name='add_pizza_in_pizza_shop')


]
