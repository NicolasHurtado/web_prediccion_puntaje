from django.urls import path
from .views import *

urlpatterns = [
    path('predict_score/', PrediccionAPIView.as_view(), name='predict_score'),
    path('', PrediccionTemplateAPIView, name='predict_score_template'),
]