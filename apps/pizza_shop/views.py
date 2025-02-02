from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.pizza_shop.serializers import PizzaShopSerializer
from apps.pizza_shop.models import PizzaShopModel
from apps.pizza.serializers import PizzaSerializer

class PizzaShopListCreateView(ListCreateAPIView):
    serializer_class = PizzaShopSerializer
    queryset = PizzaShopModel.objects.all()


class PizzaShopAddPizzaView(GenericAPIView):
    queryset = PizzaShopModel.objects.all()

    def get(self, *args, **kwargs):
        pizza_shop = self.get_object()
        serializer = PizzaShopSerializer(pizza_shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        pizza_shop = self.get_object()
        print(pizza_shop)
        data = self.request.data
        serializer = PizzaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(pizza_shop=pizza_shop)
        shop_serializer = PizzaShopSerializer(pizza_shop)
        return Response(shop_serializer.data, status=status.HTTP_201_CREATED)

