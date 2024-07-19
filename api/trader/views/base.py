from rest_framework import mixins, viewsets

# class TraderView(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     viewsets.GenericViewSet
# ):


class LViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ List ViewSet """


class CViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Create ViewSet """


class CLViewSet(LViewSet, mixins.CreateModelMixin):
    """ Create, List ViewSet """
