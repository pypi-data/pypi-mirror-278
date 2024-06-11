import snap7

class RayoCRN:
    def __init__(self):
        pass

    def connect(self,ip):
        try:
            self.s7client = snap7.client.Client()
            self.s7client.connect(ip, 1, 1)
            return self.s7client
        except Exception as ex:
            raise Exception(str(ex))

    def read_test(self,DbName,Start,Size):
        try:
            # s7client = snap7.client.Client()
            # s7client.connect("192.168.1.163", 1, 1)
            # value =s7client.db_read(DbName,Start,Size)
            return self.db_read(DbName, Start, Size)

        except Exception as ex:
            raise Exception(str(ex))