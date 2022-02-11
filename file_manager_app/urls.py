"""File manager urls"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("api/", views.StructureAPIView.as_view(), name="api"),
    path("api/<int:pk>/", views.StructureAPIView.as_view(), name="api"),
    path("", views.StructureTemplateView.as_view(), name="folders"),
    path("<int:pk>/", views.StructureTemplateView.as_view(), name="folders"),
    path("download/<int:pk>/", views.FileDownloadView.as_view(), name="files"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
