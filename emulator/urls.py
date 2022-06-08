from django.template.defaulttags import url
from django.urls import path, include
import emulator.views as views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.charger_emulator_view, name='charger_emulator_view'),
    path('provisioning/', views.provisioning, name='provisioning'),
    path('heartbeat/', views.heartbeat, name='heartbeat'),
    path('networkconfig/', views.network_config, name='network_config'),
    path('heartbeat_response/', csrf_exempt(views.heartbeat_respond), name='heartbeatresponse'),
    path('wifi_config/', csrf_exempt(views.wifi_config), name='wifi_config')
]