from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views.product import ProductView
from .views.user import UserView

router = DefaultRouter()
router.register(r'products', ProductView, basename='product')
router.register(r'users', UserView, basename='user')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
