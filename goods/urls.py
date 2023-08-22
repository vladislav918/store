from django.urls import path
from . import views
from .views import SearchResultsListView

app_name = 'goods'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
]