import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import emulator.utils as utils
from emulator.models import Charger
from .forms import ChargerForm, HeartbeatForm, SerialNumberForm
import requests

SERVER_IP = '127.0.0.1'
PORT = 8000
SERIAL_NUMBER = 32


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def provisioning(request):
    response = ''
    provisioning_form = ChargerForm()
    heartbeat_form = HeartbeatForm()

    if request.method == 'POST':
        data = {}
        serial_number_form = ChargerForm(request.POST)
        if serial_number_form.is_valid():
            SERIAL_NUMBER = serial_number_form.cleaned_data.get('serial_number')

        url = "http://" + SERVER_IP + ":" + str(PORT) + "/charger_api/provisioning/" \
              + str(SERIAL_NUMBER) + '/'

        response = utils.send_post_to_server(url, data)
        print("response:", response)

    else:
        provisioning_form = ChargerForm()
        heartbeat_form = HeartbeatForm()

    return render(request, './emulator/main.html', {'provisioning_form': provisioning_form,
                                                    'heartbeat_form': heartbeat_form,
                                                    'response': response})


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def heartbeat(request):
    response = ""
    heartbeat_form = HeartbeatForm(request.POST)
    provisioning_form = ChargerForm()
    if request.method == 'POST':
        if heartbeat_form.is_valid():
            data = heartbeat_form.cleaned_data
            SERIAL_NUMBER = data.get('serial_number')
            try:
                charger = Charger.objects.get(serial_number=data.get('serial_number'))
            except Charger.DoesNotExist:
                charger = Charger(serial_number=data.get('serial_number'))
                charger.save()

            url = "http://" + SERVER_IP + ":" + str(PORT) + "/charger_api/heartbeat/"
            response = utils.send_post_to_server(url, data)
            print("Response:", response)
    else:
        heartbeat_form = HeartbeatForm()
        serial_number_form = ChargerForm()

    return render(request, './emulator/main.html', {
        'heartbeat_form': heartbeat_form,
        'response': response,
        'provisioning_form': provisioning_form})


# @permission_classes([AllowAny])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def heartbeat_respond(request, serial_number):
#     heartbeat_form = HeartbeatForm()
#     provisioning_form = ChargerForm()
#
#     if request.method == 'POST':
#         state = request.POST.get("state")
#         operations = request.POST.get("operations")
#         print("commands:", operations)
#         try:
#             charger = Charger.objects.get(serial_number=serial_number)
#             charger.commands = operations
#             print(operations)
#
#             charger.save()
#         except Charger.DoesNotExist:
#             obj = Charger(serial_number=serial_number)
#             charger.commands = operations
#
#             obj.save()
#
#         data = {'state': state,
#                 'commands': operations}
#         print("state", state, "operations", operations)
#     else:
#         print(request)
#         charger = Charger.objects.get(serial_number=serial_number)
#         operations = charger.commands
#         data = {'operations': operations}
#         print('GET request')
#     return render(request, './emulator/main.html', {'response': data,
#                                                     'heartbeat_form': heartbeat_form,
#                                                     'provisioning_form': provisioning_form,
#                                                     })


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def network_config(request, serial_number):
    heartbeat_form = HeartbeatForm()
    serial_number_form = SerialNumberForm()
    provisioning_form = ChargerForm()

    if request.method == 'POST':

        try:
            charger = Charger.objects.get(serial_number=serial_number)
        except Charger.DoesNotExist:
            charger = Charger(serial_number=serial_number)

        charger.public_ip_address = request.POST.get("public_ip_address")
        charger.private_ip_address = request.POST.get("private_ip_address")
        charger.mac_address = request.POST.get("mac_address")
        charger.port = request.POST.get("port")
        charger.gateway = request.POST.get("gateway")
        charger.subnet_mask = request.POST.get("subnet_mask")
        charger.dns = request.POST.get("dns")
        charger.save()
        print("network config: ", charger.public_ip_address, charger.private_ip_address, charger.mac_address,
              charger.port, charger.subnet_mask, charger.gateway, charger.dns)

        return HttpResponse(json.dumps({'status': status.HTTP_200_OK}), content_type="application/json")
    else:
        if serial_number_form.is_valid():
            serial_number = request.GET.get("serial_number")
        try:
            charger = Charger.objects.get(serial_number=serial_number)
            data = {'public_ip_address': charger.public_ip_address,
                    'private_ip_address': charger.private_ip_address,
                    'mac_address': charger.mac_address,
                    'port': charger.port,
                    'gateway': charger.gateway,
                    'subnet_mask': charger.subnet_mask,
                    'dns': charger.dns}
        except Charger.DoesNotExist:
            data = {'respond': "This charger doesn't exists"}

        return render(request, './emulator/main.html', {'response': data,
                                                        'heartbeat_form': heartbeat_form,
                                                        'provisioning_form': provisioning_form,
                                                        })


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def wifi_config(request, serial_number):
    heartbeat_form = HeartbeatForm()
    provisioning_form = ChargerForm()

    if request.method == 'POST':
        wifi_ssid = request.POST.get("wifi_ssid")
        wifi_pass = request.POST.get("wifi_pass")

        print("wifi config: ", wifi_ssid, wifi_pass)
        try:
            charger = Charger.objects.get(serial_number=serial_number)
            charger.wifi_ssid = wifi_ssid
            charger.wifi_pass = wifi_pass
            charger.save()
        except Charger.DoesNotExist:
            charger = Charger(serial_number=serial_number)
            charger.wifi_ssid = wifi_ssid
            charger.wifi_pass = wifi_pass
            charger.save()
        data = {}
        return HttpResponse(json.dumps({'status': status.HTTP_200_OK}), content_type="application/json")
    else:
        print("request:", request)
        try:
            charger = Charger.objects.get(serial_number=serial_number)
            data = {'wifi_ssid': charger.wifi_ssid,
                    'wifi_pass': charger.wifi_pass,
                    }
        except Charger.DoesNotExist:
            data = {'respond': "This charger doesn't exists"}

        return render(request, './emulator/main.html', {'response': data,
                                                        'heartbeat_form': heartbeat_form,
                                                        'provisioning_form': provisioning_form,
                                                        })


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def charger_emulator_view(request):
    provisioning_form = ChargerForm()
    heartbeat_form = HeartbeatForm()
    commands_from_server = ""
    print(request.POST)

    return render(request, './emulator/main.html', {'response': 'Nothing has sent to server',
                                                    'provisioning_form': provisioning_form,
                                                    'heartbeat_form': heartbeat_form,
                                                    'commands_from_server': commands_from_server})
