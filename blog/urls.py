from django.urls import path
from django.contrib.auth import views as auth_views



from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='blog-about'),
    path('register/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('addaccount/', views.addAccount, name='addAccount'),
    path('directtransfer/', views.directTranfer, name='directtransfer'),
    path('addcredit/', views.addcredit, name='addcredit'),
    path('credittransfer/', views.pay_with_credit, name='credittransfer'),

]