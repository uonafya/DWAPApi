"""middlewareapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('api/', include("authman.urls")),
    path('api/', include("mapping_rules.urls")),
    path('api/',include('datapull.urls')),
]
# default: "Django Administration"
admin.site.site_header = 'Data IL Backend Administration'
# default: "Site administration"
admin.site.index_title = 'Backend Admin Area'
admin.site.site_title = 'Data IL Backend Administration'
