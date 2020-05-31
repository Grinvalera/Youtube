from django.urls import path
from account import views

urlpatterns = [
    path('', views.youtube, name='youtube'),
    path('registration/', views.RegisterFormView.as_view(), name='registration'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search/', views.search, name='search'),
    path('cart/<int:pk>', views.cart, name='cart'),
    path('favorite', views.favorite, name='favorite')
    # path('test/', views.test, name='test')
]




