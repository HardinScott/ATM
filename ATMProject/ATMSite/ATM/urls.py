from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('index/', views.index, name='index'),
	path('home/', views.index, name='index'),
	path('enquiry/', views.enquiry, name='enquiry'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('<int:Account_Number>/transfer/', views.transfer, name='transfer'),
	path('confirm/', views.confirm, name='confirm'),
]
