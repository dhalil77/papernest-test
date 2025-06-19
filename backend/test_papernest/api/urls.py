from django.urls import path
from api.views.views import *

urlpatterns = [
    path('coverage/', CoverageAPIView.as_view(), name='coverage'),
]