from django.urls import include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.trader import urls as trader_urls


urlpatterns = [
    re_path(r'^traders/', include(trader_urls)),
    re_path('^token/', TokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    re_path('^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
