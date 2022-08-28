"""aiapiproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include, re_path
from django.http import HttpResponse # for index page

# for swagger: start
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="AI-API",
        default_version='v1',
        description="A webservice for access to a AI-Application.",
        terms_of_service="https://github.com/haenno/ai-api",
        contact=openapi.Contact(email="haenno@web.de"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# for swagger: end

urlpatterns = [
    path('', lambda request: HttpResponse('<html><body><p><h1>This is the backend of an \
        AI-API-Application</h1><b>Proceed to</b>         <a href="doc/">doc</a>, \
        <a href="redoc/">redoc</a>, <a href="spec.json">spec.json</a>         \
        or <a href="spec.yaml">spec.yaml</a> for more details to this API.<br>\
        <br>Check <a href="https://github.com/haenno/ai-api">github.com/haenno/ai-api</a>\
        for the project documentation.</p></body></html>'), name='index'),  # for index page
    path('admin/', admin.site.urls),
    re_path(r'^spec(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # for swagger
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # for swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # for swagger
    path('api/v1/', include('aiapiapp.chatbot.urls')),
]
