import requests
from rest_framework import status
from rest_framework.response import Response
import json


def send_post_to_server(url, data):
    try:
        response = requests.post(url, data)
        response = json.loads(response.content)
        return response
        # return Response(response, status=status.HTTP_200_OK)
    except requests.exceptions.ConnectionError as errc:
        return Response(str(errc), status=status.HTTP_200_OK)
    except requests.exceptions.HTTPError as errh:
        return Response(str(errh), status=status.HTTP_200_OK)
    except requests.exceptions.Timeout as errt:
        return Response(str(errt), status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as err:
        return Response(str(err), status=status.HTTP_200_OK)


def send_get_to_server(url, data):
    try:
        response = requests.get(url, data)
        return Response(response, status=status.HTTP_200_OK)
    except requests.exceptions.ConnectionError as errc:
        return Response(str(errc), status=status.HTTP_200_OK)
    except requests.exceptions.HTTPError as errh:
        return Response(str(errh), status=status.HTTP_200_OK)
    except requests.exceptions.Timeout as errt:
        return Response(str(errt), status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as err:
        return Response(str(err), status=status.HTTP_200_OK)


def listToString(s):
    str1 = ""

    for ele in s:
        str1 += ele +", "
    str1 = str1[0:-2]
    return str1


def stringToList(s):
    l = s.split(", ")
    return l