"""
URL configuration for warehouse_pvz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path('accounts/', include("django.contrib.auth.urls")), 
    path('register/', views.register, name='register'),  # Страница регистрации нового пользователя
    path("index/", views.index, name="index"),  # Страница со списком всех ПВЗ
    path("about/<int:pvz_id>/", views.about, name="about"),  # Страница для конкретного ПВЗ с его заказами
    path("check_order/<int:order_id>/", views.check_order, name="check_order"),  # Страница для проверки и обработки конкретного заказа
    path("tracking/", views.tracking, name="tracking"),  # Страница со списком выданных заказов
    path('receipts/', views.add_receipt, name='add_receipt'),  # Страница добавления нового заказа
    path('orders/', views.order_list, name='order_list'),  # Страница со списком всех заказов
    path('success/', views.success_page, name='success_page'),  # Страница успешного выполнения действия
    path('issue_order/<int:order_id>/', views.issue_order, name='issue_order'),  # Страница для выдачи товаров из заказа
    path('issued_orders/', views.issued_orders, name='issued_orders'),  # Страница с выданными заказами
    path('purchased_items/', views.purchased_items, name='purchased_items'),  # Страница с купленными товарами
    path('returned_items/', views.returned_items, name='returned_items'),  # Страница с возвращёнными товарами
    path('export_import/', views.export_import, name='export_import'),  # Страница для экспорта данных
    path('export_orders/', views.export_orders, name='export_orders'),  # Страница для экспорта информации о выданных заказах
    path('pvz/', views.pvz_list, name='pvz_list'),  # Страница со списком всех ПВЗ
    path('pvz/add/', views.add_pvz, name='add_pvz'),  # Страница для добавления нового ПВЗ
]


