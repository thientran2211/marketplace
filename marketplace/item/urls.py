from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:item_id>/delete/', views.delete, name='delete'),
    path('<int:item_id>/edit/', views.edit, name='edit'),
]
