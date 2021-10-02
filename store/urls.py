from django.urls import path, include
from store import views 

app_name = 'store'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='store-home'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('create-checkout-session/item/<int:id>/', views.create_checkout_session, name='checkout'),
    path('success/<int:item_id>/', views.success, name='success'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
    path('item/new/', views.ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update', views.ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete', views.ItemDeleteView.as_view(), name='item-delete'),
    path('terms/', views.terms, name='terms'),
]