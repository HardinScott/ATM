from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('index/', views.index, name='index'),
	path('home/', views.index, name='index'),
	path('enquiry/', views.enquiry, name='enquiry'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('transfer/', views.transfer, name='transfer'),
	path('confirm/', views.confirm, name='confirm'),
]
