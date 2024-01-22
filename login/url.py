from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import api

urlpatterns=[
    path('sign_in/',views.sign_in,name='sign_in'),
    path('api/sign_in/',api.sign_in.as_view(),name='api_sign_in'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('api/signup/',api.signup.as_view(),name='api_signup'),
    path('sign_out/',views.sign_out,name='sign_out'),
 	
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)