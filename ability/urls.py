from django.urls import path
from .views import AbilityView, AbilityDetail

urlpatterns = [
    path('', AbilityView.as_view()),
    path('<int:pk>', AbilityDetail.as_view())
]
