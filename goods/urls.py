from django.urls import path
from .views import ProductListView, FavouritesListView, ProductCreateView, \
    SearchResultsListView, ProductDetailView, ProductUpdateView

app_name = 'goods'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('favourites/', FavouritesListView.as_view(), name='favourites'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<slug:slug>', ProductUpdateView.as_view(), name='update'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
