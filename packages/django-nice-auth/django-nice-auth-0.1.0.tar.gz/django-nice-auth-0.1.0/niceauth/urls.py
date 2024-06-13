from django.urls import path
from .views import GetNiceAuthView, GetNiceAuthUrlView, VerifyNiceAuthView

urlpatterns = [
    path('', GetNiceAuthView.as_view(), name='get_nice_auth'),
    path('url/', GetNiceAuthUrlView.as_view(), name='get_nice_auth_url'),
    path('verify/', VerifyNiceAuthView.as_view(), name='verify_auth_result'),
]
