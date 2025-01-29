from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sell_request/', views.sell_request, name='sell_request'),
    path('buy_request/', views.buy_request, name='buy_request'),
    path('vote/<int:request_type>/<int:request_id>/', views.vote_request, name='vote'),
]