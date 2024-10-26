from django.urls import path
from .views import create_rule_view, evaluate_rule_view
from .views import create_rule_view, get_all_rules_view, delete_rule_view
from . import views


urlpatterns = [
    path('create_rule/', views.create_rule_view, name='create_rule'),
    path('combine_rules/', views.combine_rules, name='combine_rules'),
    path('evaluate_rule/', views.evaluate_rule_view, name='evaluate_rule'),  # Add this line for evaluation
    path('get_all_rules/', views.get_all_rules_view, name='get_all_rules'),
    path('delete_rule/<int:rule_id>/', views.delete_rule_view, name='delete_rule'),
]
