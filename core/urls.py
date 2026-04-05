from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("about-response/", views.about_response_demo, name="about-response"),
    path("api/health/", views.api_health, name="api-health"),
    path("register/", views.register_view, name="register"),
    path("menu/", views.menu_list, name="menu-list"),
    path("menu/new/", views.menu_create, name="menu-create"),
    path("menu/<int:pk>/edit/", views.menu_update, name="menu-update"),
    path("menu/<int:pk>/delete/", views.menu_delete, name="menu-delete"),
    path("order/new/", views.place_order, name="place-order"),
    path("orders/", views.my_orders, name="my-orders"),
    path("feedback/new/", views.feedback_create, name="feedback-create"),
    path("theme/<str:theme>/", views.set_theme, name="set-theme"),
]
