from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_list, name='search_list'),
    path('search/<int:page_number>/', views.search_list, name='search_list'),
    path('upload/', views.upload_details, name='upload_details'),
    path('upload/<int:detail>/', views.upload_details, name='upload_details'),
    path('about/', views.about, name='about'),
    path('api/list/', views.list_api, name='list_api'),
    path('api/list/<int:breed_id>/', views.retrieve_api, name='retrieve_api'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
# add more breeds
# host website
