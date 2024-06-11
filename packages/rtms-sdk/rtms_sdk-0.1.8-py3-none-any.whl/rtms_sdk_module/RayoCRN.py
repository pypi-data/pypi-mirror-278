import snap7

class RayoCRN:
    def __init__(self):
        self.s7client = snap7.client.Client()

    def connect(self,ip):
        try:
            # ip = ip.encode("utf-8")
            return self.s7client.connect(ip, 1, 1)

        except Exception as ex:
            raise Exception(str(ex))

    def read_test(self,DbName,Start,Size):
        try:
            # s7client = snap7.client.Client()
            # s7client.connect("192.168.1.163", 1, 1)
            # value =s7client.db_read(DbName,Start,Size)
            return self.s7client.db_read(DbName, Start, Size)

        except Exception as ex:
            raise Exception(str(ex))