from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponseRedirect("/polls/")),  # Redirect root to /polls/ oneline funcn
]
