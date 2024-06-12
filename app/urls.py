"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path,re_path
from api import api
from api.admin import api as admin_api
from app import settings

def handle_temp_upload_file_preview(request,path):
    if not settings.DEBUG:
        return HttpResponse("Not Found", status=404)
    file_path = "temp/" + path
    white_list = ["jpg", "jpeg", "png", "gif"]

    if file_path.split(".")[-1] in white_list:
        if request.method == "GET":
            with open(file_path, "rb") as f:
                return HttpResponse(f.read(), content_type="image/%s" % file_path.split(".")[-1])
    return HttpResponse("Not Found", status=404)

urlpatterns = [
    path("admin-plane/", admin.site.urls),
    re_path(r"^api/", api.handle),
    re_path(r"^admin/api/", admin_api.handle),
    re_path(r"^temp/(?P<path>.*)$", handle_temp_upload_file_preview),
]
