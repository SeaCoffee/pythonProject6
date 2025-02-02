from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny


from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer, PizzaPhotoSerializer
from apps.pizza.filters import PizzaFilter

class PizzaListCreateView(ListAPIView):
    queryset = PizzaModel.objects.all()
    serializer_class = PizzaSerializer
    filterset_class = PizzaFilter
    permission_classes = (IsAdminUser)


class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PizzaModel.objects.all()
    serializer_class = PizzaSerializer


class PizzaAddPhotoView(UpdateAPIView):
    serializer_class = PizzaPhotoSerializer
    queryset = PizzaModel.objects.all()
    http_method_names = ['patch']
    permission_classes = (AllowAny,)

    def perform_update(self, serializer):
        pizza = self.get_object()
        pizza.photo.delete()
        super().perform_update(serializer)










