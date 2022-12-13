from django.urls import path
from darul_ekama.views import (
    SeatBookingView,
    NigraniTableView,
    SeatBooingDetail
)

urlpatterns = [
    path('<madrasha_slug>/seat-booking/', SeatBookingView.as_view()),
    path('<madrasha_slug>/darul-ekama-nigrani/', NigraniTableView.as_view()),
    path('seat-booking-detail/<int:pk>/', SeatBooingDetail.as_view()),
]
