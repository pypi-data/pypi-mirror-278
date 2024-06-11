
import snap7


def RayoCRN_Open(ip):
    try:
        #ip = ip.encode("utf-8")
        s7client = snap7.client.Client()
        s7client.connect(ip,1,1)
        return (1, "1")
    except Exception as ex:
        return (0, str(ex))

