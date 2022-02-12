"""File manager urls"""
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

SchemaView = get_schema_view(
    openapi.Info(
        title="Structure API",
        default_version="v1",
        description="Structure folder and file",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@structure.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/", views.StructureAPIView.as_view(), name="api"),
    path("api/<int:pk>/", views.StructureAPIView.as_view(), name="api"),
    path("", views.StructureTemplateView.as_view(), name="folders"),
    path("<int:pk>/", views.StructureTemplateView.as_view(), name="folders"),
    path("download/<int:pk>/", views.FileDownloadView.as_view(), name="files"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
