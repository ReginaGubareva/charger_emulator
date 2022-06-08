from django.shortcuts import render
from rest_framework.decorators import renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import emulator.utils as utils
from emulator.models import Charger
from .forms import ChargerForm, HeartbeatForm
import requests

SERVER_IP = '127.0.0.1'
PORT = 8000


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def charger_emulator_view(request):
    serial_number_form = ChargerForm()
    heartbeat_form = HeartbeatForm()
    commands_from_server = ""
    print(request.POST)

    return render(request, './emulator/main.html', {'response': 'Nothing has sent to server',
                                                    'serial_number_form': serial_number_form,
                                                    'heartbeat_form': heartbeat_form,
                                                    'commands_from_server': commands_from_server})


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def provisioning(request):
    response = ''
    if request.method == 'POST':
        print("hello world")
        data = {}
        serial_number_form = ChargerForm(request.POST)
        if serial_number_form.is_valid():
            data = serial_number_form.cleaned_data
            data = data.get('serial_number')

        url = "http://" + SERVER_IP + ":" + str(PORT) + "/charger_api/provisioning/" + str(data) + '/'

        response = utils.send_get_to_server(url, data)
        print("response:", response)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}

        print(response.rendered_content)
        print('data in Post:', data)
    else:
        serial_number_form = ChargerForm()

    return render(request, './emulator/main.html', {'serial_number_form': serial_number_form,
                                                    'response': response})


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def heartbeat(request):
    response = ""
    if request.method == 'POST':
        heartbeat_form = HeartbeatForm(request.POST)
        serial_number_form = ChargerForm()

        if heartbeat_form.is_valid():
            data = heartbeat_form.cleaned_data

            try:
                charger = Charger.objects.get(serial_number=32)
            except Charger.DoesNotExist:
                charger = Charger(serial_number=32)
                charger.save()

            url = "http://" + SERVER_IP + ":" + str(PORT) + "/charger_api/heartbeat/"
            response = utils.send_post_to_server(url, data)
            # print('response:', response)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
    else:
        heartbeat_form = HeartbeatForm()
        serial_number_form = ChargerForm()

    return render(request, './emulator/main.html', {
        'heartbeat_form': heartbeat_form,
        'response': response.data,
        'serial_number_form': serial_number_form, })


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def heartbeat_respond(request):
    heartbeat_form = HeartbeatForm()
    serial_number_form = ChargerForm()

    if request.method == 'POST':
        state = request.POST.get("state")
        operations = request.POST.get("operations")
        print("commands:", operations)
        try:
            charger = Charger.objects.get(serial_number=32)
            charger.commands = operations
            print(operations)

            charger.save()
        except Charger.DoesNotExist:
            obj = Charger(serial_number=32)
            charger.commands = operations

            obj.save()

        data = {'state': state,
                'commands': operations}
        print("state", state, "operations", operations)
    else:
        print(request)
        charger = Charger.objects.get(serial_number=32)
        operations = charger.commands
        data = {'operations': operations}
        print('GET request')
    return render(request, './emulator/main.html', {'response': data,
                                                    'heartbeat_form': heartbeat_form,
                                                    'serial_number_form': serial_number_form,
                                                    })


@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def network_config(request):
    heartbeat_form = HeartbeatForm()
    serial_number_form = ChargerForm()

    if request.method == 'POST':
        public_ip_address = request.POST.get("public_ip_address")
        private_ip_address = request.POST.get("private_ip_address")
        mac_address = request.POST.get("mac_address")
        port = request.POST.get("port")
        gateway = request.POST.get("gateway")
        subnet_mask = request.POST.get("subnet_mask"),
        dns = request.POST.get("dns")

        print("network config: ", public_ip_address, private_ip_address, mac_address,
              port, subnet_mask, gateway, dns)
        try:
            charger = Charger.objects.get(serial_number=32)
            charger.public_ip_address = public_ip_address
            charger.private_ip_address = private_ip_address
            charger.mac_address = mac_address
            charger.port = port
            charger.gateway = gateway
            charger.subnet_mask = subnet_mask
            charger.dns = dns
            charger.save()
        except Charger.DoesNotExist:
            charger = Charger(serial_number=32)
            charger.public_ip_address = public_ip_address
            charger.private_ip_address = private_ip_address
            charger.mac_address = mac_address
            charger.port = port
            charger.gateway = gateway
            charger.subnet_mask = subnet_mask
            charger.dns = dns
            charger.save()
            charger.save()

        data = {}
    else:

        try:
            charger = Charger.objects.get(serial_number=32)
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
                                                    'serial_number_form': serial_number_form,
                                                    })

@permission_classes([AllowAny])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def wifi_config(request):
    heartbeat_form = HeartbeatForm()
    serial_number_form = ChargerForm()

    if request.method == 'POST':
        wifi_ssid = request.POST.get("wifi_ssid")
        wifi_pass = request.POST.get("wifi_pass")

        print("wifi config: ", wifi_ssid, wifi_pass)
        try:
            charger = Charger.objects.get(serial_number=32)
            charger.wifi_ssid = wifi_ssid
            charger.wifi_pass = wifi_pass
            charger.save()
        except Charger.DoesNotExist:
            charger = Charger(serial_number=32)
            charger.wifi_ssid = wifi_ssid
            charger.wifi_pass = wifi_pass
            charger.save()
        data = {}


    else:
        print("request:", request)
        try:
            charger = Charger.objects.get(serial_number=32)
            data = {'wifi_ssid': charger.wifi_ssid,
                    'wifi_pass': charger.wifi_pass,
                    }
        except Charger.DoesNotExist:
            data = {'respond': "This charger doesn't exists"}

    return render(request, './emulator/main.html', {'response': data,
                                                    'heartbeat_form': heartbeat_form,
                                                    'serial_number_form': serial_number_form,
                                                    })



