from django.urls      import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static

from rest_framework.permissions import AllowAny
from drf_yasg                   import openapi, generators
from drf_yasg.views             import get_schema_view

from headtoken.views import InitView

class BothHttpAndHttpsSchemaGenerator(generators.OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema

 
schema_view = get_schema_view(
    openapi.Info(
        title="Exporterhub.io API",
        default_version='v1',
        description="Exporterhub.io API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="byoungju1012@gmail.com"),
        license=openapi.License(name="Exporterhub.io License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=BothHttpAndHttpsSchemaGenerator
)

urlpatterns = [
    path('init_done', InitView.as_view()),
    path('exporter', include('exporter.urls')),
    path('headtoken', include('headtoken.urls')),
    path('user', include('user.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    re_path(r'^swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    re_path(r'^redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]