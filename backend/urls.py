from django.contrib import admin
from django.urls import path
from buddies_api.views import buddies_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/buddies', buddies_list), # Matches your exact frontend endpoint request path!
]
