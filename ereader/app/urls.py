from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('api/v1/booklist/', BookAPIList.as_view(), name='list'),
    path('api/v1/booklist/<int:pk>/', BookAPIDetailView.as_view(), name='view'),
    path('api/v1/bookpost/', BookAPICreate.as_view(), name='post'),
    path('api/v1/bookdelete/<int:pk>', BookAPIDestroy.as_view(), name='delete'),
]