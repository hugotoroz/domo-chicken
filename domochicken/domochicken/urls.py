from django.conf.urls import handler404,handler500
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
]
handler404 = 'core.views.pagina_no_encontrada'
handler500 = 'core.views.error_servidor'
