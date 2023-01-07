from django.urls import path
from .views import (
    DivisionListView,
    DistrictListView,
    # ThanaListView,
    # PostOfficeListView,
    # PostCodeListView,
    AddressDetail,
    MadrashaView,
    MadrashaDetailView,
    UserRegistrationView,
    CustomAuthToken,
    MadrashaUserListingView,
    AvatarUpdateView,
    UserDetail,
    ThanaListViewWithDependency, PostOfficeListViewWithDependency, PostCodeListViewWithDependency, PasswordResetView,
    DistrictList, PostOfficeList, ThanaList, PostCodeList
)

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('user-detail/<int:pk>/', UserDetail.as_view()),

    # Address path
    path('division/', DivisionListView.as_view()),
    path('district/', DistrictList.as_view()),  # for backend dependable newly added on 7
    # path('district/', DistrictListView.as_view()),
    path('district/<division>/', DistrictListView.as_view()),

    path('thana/', ThanaList.as_view()),  # for backend dependable newly added on 7
    # path('thana/', ThanaListView.as_view()),
    path('thana/<district>/', ThanaListViewWithDependency.as_view()),

    path('post-office/', PostOfficeList.as_view()),  # for backend dependable newly added on 7
    # path('post-office/', PostOfficeListView.as_view()),
    path('post-office/<district>/', PostOfficeListViewWithDependency.as_view()),
    path('post-code/', PostCodeList.as_view()),  # for backend dependable newly added on 7
    # path('post-code/', PostCodeListView.as_view()),
    path('post-code/<post_office>/', PostCodeListViewWithDependency.as_view()),
    path('address/<int:pk>/', AddressDetail.as_view()),

    # madrasha path
    path('madrasha/', MadrashaView.as_view()),
    path('madrasha/detail/<slug:slug>/', MadrashaDetailView.as_view()),
    path('madrasha-admin/', UserRegistrationView.as_view()),
    path('mu-listing/', MadrashaUserListingView.as_view()),
    path('avatar/<int:pk>/', AvatarUpdateView.as_view()),

    # password reset
    path('madrasha-admin-pass-reset/<user_id>/', PasswordResetView.as_view())
]
