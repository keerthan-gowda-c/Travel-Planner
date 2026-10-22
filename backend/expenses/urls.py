from django.urls import path
from .views import ExpenseListCreateView,ExpenseSummaryView

urlpatterns = [
    path("",ExpenseListCreateView.as_view(), name="expense-list-create"),
   path("trips/<str:trip_title>/summary/",ExpenseSummaryView.as_view(),name="expense-summary"),
]