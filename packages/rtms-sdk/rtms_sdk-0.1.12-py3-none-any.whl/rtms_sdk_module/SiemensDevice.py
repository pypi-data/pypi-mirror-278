import snap7

class SiemensDevice:
    IsConnect = False  #是否连接
    RetryCurrentNumber = 0  #当前重试连接次数
    RetryMaxNumber = 3      #重试连接最大次数
    CurrentRead = 0
    PlcIP = ""
    PlcNrock = 0
    PlcNslot = 0
    SiemensPLC = None
    crnNo = 0

    def __init__(self):
        pass

    #PLC连接
    def connect(self,IP, crnNo, forkCount=1):
        if self.IsConnect:
            self.SiemensPLC.disconnect()
        try:
            self.SiemensPLC = snap7.client.Client()
            self.PlcIP = IP
            self.PlcNrock = 0
            self.PlcNslot = 0
            self.SiemensPLC.connect(self.PlcIP, self.PlcNrock, self.PlcNslot)
            self.IsConnect = True
            self.RetryCurrentNumber = 0
            self.CurrentRead = 0
            self.ForkNumber = forkCount
            self.crnNo = crnNo
            return True
        except Exception as ex:
            raise Exception(str(ex))

    #PLC重连
    def retryOpen(self):
        try:
            if not self.IsConnect:
                self.SiemensPLC.disconnect()
                self.RetryCurrentNumber += 1
                self.SiemensPLC.connect(self.PlcIP, self.PlcNrock, self.PlcNslot)
                self.IsConnect = True
                self.RetryCurrentNumber = 0
            return True
        except Exception as ex:
            if self.RetryCurrentNumber > self.RetryMaxNumber:  # 达到最大值终止重连
                raise Exception("重连次数达到最大值:" + str(self.RetryMaxNumber))
            raise Exception("第 " + str(self.RetryCurrentNumber) + "次重连失败:" + str(ex))

    #PLC读DB数据
    def readDb(self,DbName,Start,Size):
        try:
            self.retryOpen()
            return self.SiemensPLC.db_read(DbName, Start, Size)
        except Exception as ex:
            raise Exception(str(ex))

    #PLC写DB数据
    def writeDb(self,DbName,Start,Data):
        try:
            self.retryOpen()
            return self.SiemensPLC.db_write(DbName, Start, Data)
        except Exception as ex:
            raise Exception(str(ex))