from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('terms/',views.terms,name='terms'),
    path('contact/',views.contact_page,name='contact'),
    path('warrenty/',views.warrenty,name='warrenty'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logoutP,name='logout'),
    path('register/',views.register,name='register'),
    path('newsletter/',views.newsletter_sub,name='newsletter'),
    path('partnership/',views.partnership_form,name='partnership'),
    path('search/',views.SearchDataView,name='search'),
    path('product_page_single/<str:pk>',views.product_page_single,name='product_page_single'),
    path('add_to_watchlist/<str:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_watchlist/<str:pk>/', views.remove_watchlist, name='remove_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('filter_search/', views.filter_search, name='filter_search'),
    path('sema2018/', views.sema2018, name='sema2018'),
    path('sema2019/', views.sema2019, name='sema2019'),

    path('initial_data/', views.initial_data, name='initial_data'),
    path('market_filter/', views.market_filter, name='market_filter'),
    path('model_filter/', views.model_filter, name='model_filter'),
    path('body_filter/', views.body_filter, name='body_filter'),
    path('year_filter/', views.year_filter, name='year_filter'),
    path('suspension_filter/', views.suspension_filter, name='suspension_filter'),

    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),   
    path('cart/', views.cart, name='cart'),
    path('remove_cart/<str:pk>/', views.remove_cart, name='remove_cart'),

    path('add_order/', views.add_order, name='add_order'), 
    path('my_order/', views.my_order, name='my_order'), 
    path('order_approval/<str:pk>/', views.order_approval, name='order_approval'), 
    path('order_disapproval/<str:pk>/', views.order_disapproval, name='order_disapproval'), 
    path('all_orders/', views.all_orders, name='all_orders'),
    path('order_detail/<str:pk>/', views.order_detail, name='order_detail'), 

    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)