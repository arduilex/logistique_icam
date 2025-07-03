from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    
    # Reports
    path('reports/stock/', views.stock_report, name='stock_report'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/transactions/', views.transaction_history, name='transaction_history'),
    
    # Exports
    path('export/stock.csv', views.export_stock_csv, name='export_stock_csv'),
    path('export/sales.csv', views.export_sales_csv, name='export_sales_csv'),
    path('export/transactions.csv', views.export_transactions_csv, name='export_transactions_csv'),
]