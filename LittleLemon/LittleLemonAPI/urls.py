from django.urls import path
from .views import GroupManagementViews, MenuItemViews, CartViews, OrderViews

urlpatterns = [
    # Menu Items
    path('menu-items', MenuItemViews.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemViews.SingleMenuItemView.as_view()),
    # Group Management
    path('groups/manager/users', GroupManagementViews.group_management_managers),
    path('groups/manager/users/<int:user_id>', GroupManagementViews.group_management_managers),
    path('groups/delivery-crew/users', GroupManagementViews.group_management_delivery_crew),
    path('groups/delivery-crew/users/<int:user_id>', GroupManagementViews.group_management_delivery_crew),
    # Cart
    path('cart/menu-items', CartViews.CartView.as_view()),
    # Order
    path('orders', OrderViews.OrdersView.as_view()),
]

