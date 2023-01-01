from django.urls import path
from .views import (
    StudentView,
    StudentDetailView,
    CheckUniquePassportNumber,
    CheckUniqueNIDNumber,
    StudentDetailBySlugView, OldStudentUpdateView
)

urlpatterns = [
    path('<int:madrasha_slug>/', StudentView.as_view()),
    path('detail/<madrasha_slug>/<slug:slug>/', StudentDetailView.as_view()),
    path('detail/old-student/<madrasha_slug>/<slug:slug>/', OldStudentUpdateView.as_view()),
    path('detail-by-id/<str:student_id>/<madrasha_slug>/', StudentDetailBySlugView.as_view()),
    path('check-passport/<str:passport_number>/', CheckUniquePassportNumber.as_view()),
    path('check-nid/<str:nid_number>/', CheckUniqueNIDNumber.as_view()),
]
