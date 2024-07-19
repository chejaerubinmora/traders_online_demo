from rest_framework import (decorators,
                            mixins,
                            permissions,
                            viewsets)

from api.trader.models import Product
from api.trader.serializers import (ProductSerializer,
                                    ProductStoreSerializer,
                                    OrderSerializer,
                                    ProductRevenueSerializer)


class ProductView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['revenue', 'orders']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ['order', 'orders']:
            return OrderSerializer
        if self.action == 'revenue':
            return ProductRevenueSerializer
        if self.action == 'create':
            return ProductStoreSerializer
        return ProductSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.queryset = self.queryset.filter(user=request.user)
        return super().retrieve(request, *args, **kwargs)

    @decorators.action(detail=False, methods=['post'])
    def order(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @decorators.action(detail=True, methods=['get'])
    def orders(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.queryset.filter(
                user=request.user).first()
            self.queryset = product.order_set.all()
        return super().list(request, *args, **kwargs)

    @decorators.action(detail=True, methods=['get'])
    def revenue(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.queryset = self.queryset.filter(user=request.user)
        return super().retrieve(request, *args, **kwargs)
