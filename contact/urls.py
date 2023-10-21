from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.index, name='index'),
    
    # CRUD - Contact
    path('contact/detail/<int:contact_id>/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'),
    path('contact/update/<int:contact_id>/', views.update, name='update'),
    path('contact/delete/<int:contact_id>/', views.delete, name='delete'),
    
    path('user/register/', views.register, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
]