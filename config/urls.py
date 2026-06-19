from django.contrib import admin  # type: ignore[reportMissingModuleSource]
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # ✅ API routes
    path('api/', include('api.urls')),
]