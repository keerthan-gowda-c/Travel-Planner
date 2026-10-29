from django.urls import path
from .views import ExpenseListCreateView,ExpenseSummaryView, ExpenseDetailView

urlpatterns = [
    path("",ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("trips/<str:trip_title>/summary/",ExpenseSummaryView.as_view(),name="expense-summary"),
    path("trips/<str:expense_id>/",ExpenseDetailView.as_view(),name="expense-detail"),

]