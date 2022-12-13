from django.urls import path
from . import views

urlpatterns = [

    path('<madrasha_slug>/vehicle-info-list/', views.VehicleInfoListView.as_view()),
    path('vehicle-info/details/<int:pk>/', views.VehicleInfoDetail.as_view()),

    path('<madrasha_slug>/transport-list/', views.TransportListView.as_view()),
    path('<madrasha_slug>/post-transport/<student_id>/', views.TransportPostrequestView.as_view()),
    path('details/<int:pk>/', views.TransportDetailView.as_view()),
]
