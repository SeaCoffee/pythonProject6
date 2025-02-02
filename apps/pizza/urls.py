from django.urls import path

from apps.pizza.views import PizzaListCreateView, PizzaRetrieveUpdateDestroyView, PizzaAddPhotoView

urlpatterns = [
    path("", PizzaListCreateView.as_view(), name='pizza_add_pizza'),
    path('/<int:pk>', PizzaRetrieveUpdateDestroyView.as_view(), name='pizza_update_pizza'),
    path('/<int:pk>/photos', PizzaAddPhotoView.as_view(), name='pizza_add_photo')
]
