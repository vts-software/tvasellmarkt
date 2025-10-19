from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # стандартная админка Django
    # path('', include('shop.urls')),  # позже сюда подключим urls приложения shop
    # path('users/', include('users.urls')),  # позже подключим urls приложения users
]

# раздача медиа-файлов в режиме разработки
# DEBUG=True позволяет Django обслуживать изображения локально
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
]
