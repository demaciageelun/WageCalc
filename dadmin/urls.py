from dadmin import admin
from dadmin.admin import admin_site
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('myadmin/', admin_site.urls),
    # path('captcha/', include('captcha.urls')),
]
