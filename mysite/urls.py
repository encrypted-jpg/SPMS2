"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "mysite"
urlpatterns = [
    path("", views.index, name="index"),
    path("compPage/", include(("apps.compPage.urls", "apps.compPage"))),
    path("coursePage/", include(("apps.coursePage.urls", "apps.coursePage"))),
    path("login/", include(("apps.login.urls", "apps.login"))),
    path("partyPage/", include(("apps.partyPage.urls", "apps.partyPage"))),
    path("signUp/", include(("apps.signUp.urls", "apps.signUp"))),
    path(
        "suggestionPortal/",
        include(("apps.suggestionPortal.urls", "apps.suggestionPortal")),
    ),
    path("userPortal/", include(("apps.userPortal.urls", "apps.userPortal"))),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
