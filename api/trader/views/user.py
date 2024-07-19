from rest_framework import mixins, permissions, viewsets  # , decorators

from django.contrib.auth.models import User
from api.trader.serializers import UserSerializer, RegisterUserSerializer


class UserView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action != 'create':
            return (permissions.IsAuthenticated(), )
        return super().get_permissions()
