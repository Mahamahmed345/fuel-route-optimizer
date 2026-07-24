from django.urls import path
from .views import route_view,home

urlpatterns = [
    path('', home),
    path(
        "route/",
        route_view
    )
]