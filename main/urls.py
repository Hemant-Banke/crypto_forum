from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('pwabuilder-sw.js', views.sw, name='sw'),
    path('offline.html', views.offline, name='offline'),
    path('.well-known/assetlinks.json', views.assetlinks, name='assetlinks'),

    # Index
    path('', views.index, name='index'),
    path('platform/<str:name>', views.platform, name='platform'),
    path('platforms/<str:filter>', views.platforms_filter, name='platforms_filter'),

    path('addresses', views.addresses, name='addresses'),

    # Static
    path('support', views.support, name='support'),

    # Requests
    path('controller/register_requests', views.register_requests, name='register_requests'),
    path('controller/register_review', views.register_review, name='register_review'),
    path('controller/register_comment', views.register_comment, name='register_comment'),
    path('controller/register_address', views.register_address, name='register_address'),

    # Read Requests
    path('controller/get_search', views.get_search, name='get_search'),
    path('controller/get_recent', views.get_recent, name='get_recent'),
    path('controller/get_top_exchanges', views.get_top_exchanges, name='get_top_exchanges'),
    path('controller/get_top_coins', views.get_top_coins, name='get_top_coins'),
    path('controller/get_top_ga', views.get_top_ga, name='get_top_ga'),

    # Saves
    path('controller/get_last_saved', views.get_last_saved, name='get_last_saved'),
    path('controller/get_all_saved_coins', views.get_all_saved_coins, name='get_all_saved_coins'),
    path('controller/get_coin_saved', views.get_coin_saved, name='get_coin_saved'),

    path('controller/del_address', views.del_address, name='del_address'),

    # Read filtered by offsets
    path('controller/get_filter/<str:filter>/<int:page>', views.get_filter, name='get_filter'),
    path('controller/get_reviews/<str:plt>/<int:filter>/<int:page>', views.get_reviews, name='get_reviews'),
    path('controller/get_comments/<int:parent>', views.get_comments, name='get_comments'),

]