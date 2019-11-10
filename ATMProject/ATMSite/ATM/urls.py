from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'ATM'

urlpatterns = [
	path('', views.homepage, name='homepage'),
	path('index/', views.index, name='index'),
	path('enquiry/', views.enquiry, name='enquiry'),
	path('withdraw/', views.withdraw, name='withdraw'),
	path('transfer/', views.transfer, name='transfer'),
	path('confirm/', views.confirm, name='confirm'),
	path('logout/', views.logout_request, name='logout'),
	path('login/', views.login_request, name='login'),
]
