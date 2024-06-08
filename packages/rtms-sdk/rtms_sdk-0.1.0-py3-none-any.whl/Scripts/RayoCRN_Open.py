
from Scripts.s7 import client


def RayoCRN_Open(ip):
    try:
        ip = ip.encode("utf-8")
        client.Client.connect(ip)
        return (1, "1")
    except Exception as ex:
        return (0, str(ex))