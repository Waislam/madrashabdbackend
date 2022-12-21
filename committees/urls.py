from django.urls import path
from . import views

urlpatterns = [
    path('<madrasha_slug>/list/', views.CommitteeListView.as_view()),
    path('details/<int:pk>/', views.CommitteeDetail.as_view()),

    path('<madrasha_slug>/permanent-members/', views.PermanentMembersListView.as_view()),
    path('permanent-members/details/<int:pk>/', views.PermanentMembersDetail.as_view()),
    path('permanent-members/<phone_number>/details/', views.PermanentMembersDetailsWithPhoneFilter.as_view()),

    path('<madrasha_slug>/other-members/', views.OtherMembersListView.as_view()),
    path('other-member/details/<int:pk>/', views.OtherMembersDetail.as_view()),
]
