from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.group_management_managers),
    path('groups/manager/users/<int:user_id>', views.group_management_managers),
    path('groups/delivery-crew/users', views.group_management_delivery_crew),
    path('groups/delivery-crew/users/<int:user_id>', views.group_management_delivery_crew),
]

