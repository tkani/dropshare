from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import api


urlpatterns=[
    path('datahouse/',views.datahouse,name='datahouse'),
    path('create_folder/',views.create_folder,name='create_folder'),
    path('api/create_folder/', api.create_folder.as_view(), name='create_folder'),
    path('view_folder/<str:folder_token>',views.view_folder,name='view_folder'),
    path('collab/<str:folder_token>',views.collab,name='collab'),
    path('api/collab_folder_view/', api.collab_folder_view.as_view(), name='collab_folder_view'),
    # path('download_files/<str:file_name>/<str:save_name>', views.download_files, name='download_files'),
    path('api/collab_folder/', api.collab_folder.as_view(), name='collab_folder'),
    path('api/folder_view/', api.folder_view.as_view(), name='folder_view'),
    path('api_download_files/', api.api_download_files.as_view(), name='api_download_files'),
    path('api/data_house/',api.data_house.as_view(),name='api_data_house'),
    path('api/get_secured_file/',api.get_secured_file.as_view(),name='api_get_secured_file'),
    path('api/get_shared_file/',api.get_shared_file.as_view(),name='api_get_shared_file'),
    path('api/get_shared_folder/',api.get_shared_folder.as_view(),name='api_get_shared_folder'),
    path('api/delete_file/',api.delete_file.as_view(),name='api_delete_file'),
    path('api/user_details/',api.user_details.as_view(),name='api_user_details'),
    path('api/delete_folder/',api.delete_folder.as_view(),name='api_delete_folder'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)