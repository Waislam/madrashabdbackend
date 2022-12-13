from django.urls import path
from .views import KhabarDistributionView, DailyBazarView, DailyBazarDetailView

urlpatterns = [
    # path('bazarlist/<madrasha_slug>/', BazarListView.as_view()),
    path('bazarlist/<madrasha_slug>/', DailyBazarView.as_view()),
    path('bazarlist/detail/<int:pk>/', DailyBazarDetailView.as_view()),
    path('khabar-distribution/<madrasha_slug>/<student_id>/<meal_id>/<date>/', KhabarDistributionView.as_view()),
]
