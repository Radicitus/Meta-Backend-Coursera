from django.urls import path
from .views import GroupManagementViews, MenuItemViews

urlpatterns = [
    path('menu-items', MenuItemViews.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemViews.SingleMenuItemView.as_view()),
    path('groups/manager/users', GroupManagementViews.group_management_managers),
    path('groups/manager/users/<int:user_id>', GroupManagementViews.group_management_managers),
    path('groups/delivery-crew/users', GroupManagementViews.group_management_delivery_crew),
    path('groups/delivery-crew/users/<int:user_id>', GroupManagementViews.group_management_delivery_crew),
]

