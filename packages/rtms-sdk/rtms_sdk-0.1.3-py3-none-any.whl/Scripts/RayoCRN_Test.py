import snap7


def RayoCRN_Test(DbName,Start,Size):
    try:
        #s7client = snap7.client.Client()
        #s7client.connect("192.168.1.163", 1, 1)
        #value =s7client.db_read(DbName,Start,Size)
        value = snap7.client.Client.db_read(DbName,Start,Size)
        return (1, value)
    except Exception as ex:
        return (0, str(ex))

