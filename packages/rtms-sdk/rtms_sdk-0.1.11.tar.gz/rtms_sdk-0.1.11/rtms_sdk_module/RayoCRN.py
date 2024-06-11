import snap7

class RayoCRN:
    IsOpen = False
    reopen_current_number = 0
    CurrentRead = 0
    __PLC_IP = ""
    __PLC_nRock = 0
    __PLC_nSlot = 0
    __PulseWidth = 0.1  # 100mS
    SiemensPLC = None
    crnNo = 0
    reopen_MaxNumber=3

    def __init__(self):
        pass

    def connect(self,IP, crnNo, forkCount=1):
        if self.IsOpen:
            self.SiemensPLC.disconnect()
        try:
            self.SiemensPLC = snap7.client.Client()
            self.__PLC_IP = IP
            self.__PLC_nRock = 0
            self.__PLC_nSlot = 0
            self.SiemensPLC.connect(self.__PLC_IP, self.__PLC_nRock, self.__PLC_nSlot)
            self.IsOpen = True
            self.reopen_current_number = 0
            self.CurrentRead = 0
            self.ForkNumber = forkCount
            self.crnNo = crnNo

            return True
        except Exception as ex:
            raise Exception(str(ex))

    def ReOpen(self):
        try:
            if not self.IsOpen:
                self.SiemensPLC.disconnect()
                # self.SiemensPLC = MySnap7()
                self.reopen_current_number += 1  # 重连次数+1

                self.SiemensPLC.connect(self.__PLC_IP, self.__PLC_nRock, self.__PLC_nSlot)
                self.IsOpen = True
                self.reopen_current_number = 0
            return True
        except Exception as ex:
            if self.reopen_current_number > self.reopen_MaxNumber:  # 达到最大值终止重连
                raise Exception("重连次数达到最大值:" + str(self.reopen_MaxNumber))
            raise Exception("第 " + str(self.reopen_current_number) + "次重连失败:" + str(ex))


    def read_test(self,DbName,Start,Size):
        try:
            self.ReOpen()
            return self.SiemensPLC.db_read(DbName, Start, Size)

        except Exception as ex:
            raise Exception(str(ex))