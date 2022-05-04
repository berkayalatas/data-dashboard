from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.expense_delete, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense_category_summary', views.expense_category_summary , name='expense_category_summary'),
    path('expense_stats', views.expense_stats_view, name='expense_stats'),
    path('export-csv', views.export_csv , name='export_csv'),
    path('export-excel', views.export_excel , name='export_excel'),
]