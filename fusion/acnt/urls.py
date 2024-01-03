from django.urls import path
from .views import ClientRegisterView,FreelanceRegisterView,ClientLoginView,FreelancerLoginView


urlpatterns = [
    path('client-register/',ClientRegisterView.as_view(),name = 'Cregister'),
    path('freelancer-register/',FreelanceRegisterView.as_view(),name = 'Fregister'),
    path('client-login/',ClientLoginView.as_view(),name = 'Clogin'),
    path('freelance-login/',FreelancerLoginView.as_view(),name = 'Flogin'),
]
