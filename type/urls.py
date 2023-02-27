from django.urls import path
from .views import TypeView, TypeDetail

urlpatterns = [
    path('', TypeView.as_view()),
    path('<int:pk>', TypeDetail.as_view()),
]