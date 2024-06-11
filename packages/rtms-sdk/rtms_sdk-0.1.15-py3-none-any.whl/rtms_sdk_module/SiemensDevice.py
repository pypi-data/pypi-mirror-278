# 西门子版本
import snap7
import binascii
import struct
import time
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import random
import threading
from Exception.CRNCommError import CRNCommError
from Exception.CRNTaskError import CRNTaskError
from Exception.CRNWriteDataError import CRNWriteDataError
from Exception.CRNWarningException import CRNWarningException
from Service.MySnap7 import MySnap7
from Const.SiemensCrnConst import SiemensCrnConst



class SiemensDevice:

    online = False  # 联机标志 1-联机 0-脱机
    fork1_middle = False  # 中位标志 1-已回中 0-未回中
    fork2_middle = False  # 中位标志 1-已回中 0-未回中
    x_real_position = 0  # 行走轴实时坐标（激光测距）mm
    y_real_position = 0  # 提升轴实时坐标（激光测距）mm
    fork1_real_position = 0  # 货叉1实时坐标mm
    fork2_real_position = 0  # 货叉2实时坐标mm
    fork1_layer = 0  # 货叉1当前所在层
    fork1_col = 0  # 货叉1当前所在列
    fork2_layer = 0  # 货叉2当前所在层
    fork2_col = 0  # 货叉2当前所在列
    state = 0  # 堆垛机当前状态
    fork1_task_step = 0  # 货叉1任务步骤
    fork2_task_step = 0  # 货叉2任务步骤
    fork1_doing_taskCode = 0  # 货叉1正在执行任务号
    fork2_doing_taskCode = 0  # 货叉2正在执行任务号
    fork1_finish_taskCode = 0  # 货叉1已完成任务号
    fork2_finish_taskCode = 0  # 货叉2已完成任务号
    fork1_occupy = 0  # 货叉1当前占位
    fork2_occupy = 0  # 货叉2当前占位
    fork1_storge_outside_occupy = 0  # 货叉1当前外侧库位占位
    fork2_storge_outside_occupy = 0  # 货叉2当前外侧库位占位
    fork1_storge_inside_occupy = 0  # 货叉1当前内侧库位占位
    fork2_storge_inside_occupy = 0  # 货叉2当前内侧库位占位
    x_speed = 0  # 行走轴速度
    y_speed = 0  # 提升轴速度
    fork1_speed = 0  # 货叉1当前速度
    fork2_speed = 0  # 货叉2当前速度
    error_code = 0  # 故障代码
    x_error_code = 0  # 行走轴故障代码
    x_warn_code = 0  # 行走轴报警代码
    y_error_code = 0  # 提升轴故障代码
    y_warn_code = 0  # 提升轴报警代码
    fork1_error_code = 0  # 货叉1故障代码
    fork1_warn_code = 0  # 货叉1报警代码
    fork2_error_code = 0  # 货叉2故障代码
    fork2_warn_code = 0  # 货叉2报警代码

    fork_trigger = 0  # 货叉触发类型
    taskType1 = 0  # 货叉1任务类型
    taskType2 = 0  # 货叉2任务类型
    taskCode1 = 0  # 货叉1任务号
    taskCode2 = 0  # 货叉2任务号
    fork1_pick_layer = 0  # 货叉1取货层
    fork1_pick_col = 0  # 货叉1取货列
    fork1_pick_dire = 0  # 货叉1取货排
    fork1_release_layer = 0  # 货叉1放货层
    fork1_release_col = 0  # 货叉1放货列
    fork1_release_dire = 0  # 货叉1放货排
    fork2_pick_layer = 0  # 货叉2取货层
    fork2_pick_col = 0  # 货叉2取货列
    fork2_pick_dire = 0  # 货叉2取货排
    fork2_release_layer = 0  # 货叉2放货层
    fork2_release_col = 0  # 货叉2放货列
    fork2_release_dire = 0  # 货叉2放货排

    lock = threading.Lock()
    log = True
    IsOpen = False
    SiemensPLC = None
    HeartBeatEvent = None        # 线程对象
    HeartBeatThreadFlag = False  # 线程运行标志
    HeartTimeSleep = 1
    HeartWrite = 1
    __PLC_IP = ""
    __PLC_nRock = 0
    __PLC_nSlot = 0
    __PulseWidth = 0.1  # 100mS
    reopen_current_number = 0
    reopen_MaxNumber = 100
    MaxDaysEnable = True
    MaxDays = 7
    WcsTaskCode = 0
    crnNo = 0
    CurrentRead = 0

    CRNErrorStateList = SiemensCrnConst.getCRNErrorStateList()

    CRNWarning = SiemensCrnConst.getCRNWarning()

    Dire_WMS_To_CRN = {
        1: {
            0: 0,
            1: 1,
            2: 2,
        },
        2: {
            0: 0,
            3: 1,
            4: 2,
        }
    }

    ForkTrigger = (0, 1, 2, 3, 4, 5)  # 货叉触发类型
    TaskTypeList = (0, 3, 4, 7, 8, 9)  # wcs任务类型
    ForkNumber = 2  # 货叉最大数量

    def __init__(self):
        # self.LoadXML()
        pass

    def LoadXML(self):
        path = os.getcwd()
        FileName = path+"\\CRNToolsConfig.xml"
        tree = ET.parse(FileName)
        root = tree.getroot()
        for stu in root:
            if stu.tag == "CRNWarning":
                for i in stu:
                    b = i.attrib
                    self.CRNWarning[int(b["id"])] = b["text"]

    @staticmethod
    def StrToHex(Str):
        """
        将16进制字符串转换成16进制字节序列

        :param Str: "0064"
        :return: bytes \x00 \x64
        """
        Str = ''.join(Str)
        Rlt = binascii.a2b_hex(Str)
        return Rlt

    @staticmethod
    def strTobytearray(Data):
        """
        将16进制字符串转换成16进制字节数组

        :param Data: "0064"
        :return: bytearray(b' \x00 \x64)
        """
        Data1 = SiemensDevice.StrToHex(Data)
        Val = bytearray(Data1)
        return Val

    @staticmethod
    def strToFloat(Data):
        """
        将16进制字符串转换成浮点数

        :param Data: "414570A4"
        :return: 11.24
        """
        Data1 = SiemensDevice.StrToHex(Data)
        Val = bytearray(Data1)
        return "%.3f" % struct.unpack("!f", Val)

    @staticmethod
    def bytearrayTostr(Data):
        """
        将16进制字节数组转换成16进制字符串

        :param Data: 例如bytearray('hello')
        :return: "68656c6c6f"
        """
        Data1 = binascii.b2a_hex(Data)
        Data2 = Data1.decode("utf-8")
        return Data2

    def Open(self, IP, crnNo, forkCount=1):
        """
        连接堆垛机PLC

        :param IP: IP地址
        :param crnNo: 堆垛机编号（用于转换左右排）
        :param forkCount: 货叉数量
        :return:
        """
        if self.IsOpen:
            self.SiemensPLC.disconnect()
        try:
            self.SiemensPLC = MySnap7()
            self.__PLC_IP = IP
            self.__PLC_nRock = 0
            self.__PLC_nSlot = 0
            self.SiemensPLC.connect(self.__PLC_IP, self.__PLC_nRock, self.__PLC_nSlot)
            self.IsOpen = True
            self.reopen_current_number = 0
            self.CurrentRead = 0
            self.ForkNumber = forkCount
            self.crnNo = crnNo
            # self.HeartBeatEvent = threading.Thread(target=self.__HeartBeatThread)
            # self.HeartBeatEvent.daemon = True
            # self.HeartBeatEvent.start()
            # self.HeartBeatThreadFlag = True
            return True
        except Exception as ex:
            raise CRNCommError(str(ex))

    # 心跳
    def __HeartBeatThread(self):
        """
        发送心跳获取数据

        :return:
        """
        try:
            self.WriteDBBit(1001, 34, 2, self.HeartWrite)
            self.HeartWrite = 0 if self.HeartWrite else 1
            PLCData = self.ReadDB(1000, 0, 85)[1]
            byte0 = int(PLCData[0:2], 16)
            with self.lock:
                self.online = byte0 & 0x01 == 0x01                           # 联机标志 1-联机 0-脱机
                self.fork1_middle = byte0 & 0x02 == 0x02                      # 中位标志 1-已回中 0-未回中
                self.fork2_middle = byte0 & 0x04 == 0x04                      # 中位标志 1-已回中 0-未回中
                self.x_real_position = SiemensDevice.strToFloat(PLCData[4:12])         # 行走轴实时坐标（激光测距）mm
                self.y_real_position = SiemensDevice.strToFloat(PLCData[12:20])        # 提升轴实时坐标（激光测距）mm
                self.fork1_real_position = SiemensDevice.strToFloat(PLCData[20:28])    # 货叉1实时坐标mm
                self.fork2_real_position = SiemensDevice.strToFloat(PLCData[28:36])    # 货叉2实时坐标mm
                self.fork1_layer = int(PLCData[36:40], 16)                   # 货叉1当前所在层
                self.fork1_col = int(PLCData[40:44], 16)                     # 货叉1当前所在列
                self.fork2_layer = int(PLCData[44:48], 16)                   # 货叉2当前所在层
                self.fork2_col = int(PLCData[48:52], 16)                     # 货叉2当前所在列
                self.state = int(PLCData[52:56], 16)                         # 堆垛机当前状态
                self.fork1_task_step = int(PLCData[56:60], 16)               # 货叉1任务步骤
                self.fork2_task_step = int(PLCData[60:64], 16)               # 货叉2任务步骤
                self.fork1_doing_taskCode = int(PLCData[64:68], 16)          # 货叉1正在执行任务号
                self.fork2_doing_taskCode = int(PLCData[68:72], 16)          # 货叉2正在执行任务号
                self.fork1_finish_taskCode = int(PLCData[72:76], 16)         # 货叉1已完成任务号
                self.fork2_finish_taskCode = int(PLCData[76:80], 16)         # 货叉2已完成任务号
                self.fork1_occupy = int(PLCData[80:84], 16)                  # 货叉1当前占位   ==货叉上当前是否有货
                self.fork2_occupy = int(PLCData[84:88], 16)                  # 货叉2当前占位
                self.fork1_storge_outside_occupy = int(PLCData[88:92], 16)   # 货叉1当前库位占位
                self.fork2_storge_outside_occupy = int(PLCData[92:96], 16)   # 货叉2当前库位占位
                self.fork1_storge_inside_occupy = int(PLCData[96:100], 16)   # 货叉1当前内侧库位占位
                self.fork2_storge_inside_occupy = int(PLCData[100:104], 16)  # 货叉2当前内侧库位占位
                self.x_speed = SiemensDevice.strToFloat(PLCData[104:112])              # 行走轴速度
                self.y_speed = SiemensDevice.strToFloat(PLCData[112:120])              # 提升轴速度
                self.fork1_speed = SiemensDevice.strToFloat(PLCData[120:128])          # 货叉1当前速度
                self.fork2_speed = SiemensDevice.strToFloat(PLCData[128:136])          # 货叉2当前速度
                self.error_code = int(PLCData[136:140], 16)                  # 故障代码
                self.x_error_code = int(PLCData[140:144], 16)                # 行走轴故障代码
                self.x_warn_code = int(PLCData[144:148], 16)                 # 行走轴报警代码
                self.y_error_code = int(PLCData[148:152], 16)                # 提升轴故障代码
                self.y_warn_code = int(PLCData[152:156], 16)                 # 提升轴报警代码
                self.fork1_error_code = int(PLCData[156:160], 16)            # 货叉1故障代码
                self.fork1_warn_code = int(PLCData[160:164], 16)             # 货叉1报警代码
                self.fork2_error_code = int(PLCData[164:168], 16)            # 货叉2故障代码
                self.fork2_warn_code = int(PLCData[168:172], 16)             # 货叉2报警代码
        except Exception as ex:
            self.IsOpen = False
            print(str(ex))
            raise ex

    def ReOpen(self):
        try:
            if not self.IsOpen:
                self.SiemensPLC.disconnect()
                # self.SiemensPLC = MySnap7()
                self.reopen_current_number += 1  # 重连次数+1
                if self.log:
                    self.Datalog("开始第 " + str(self.reopen_current_number) + " 次重连")
                self.SiemensPLC.connect(self.__PLC_IP, self.__PLC_nRock, self.__PLC_nSlot)
                self.IsOpen = True
                self.reopen_current_number = 0
            return True
        except Exception as ex:
            if self.reopen_current_number > self.reopen_MaxNumber:  # 达到最大值终止重连
                if self.log:
                    self.Datalog("重连次数达到最大值" + str(self.reopen_MaxNumber))
                raise CRNWarningException("重连次数达到最大值:" + str(self.reopen_MaxNumber))
            raise CRNCommError("第 " + str(self.reopen_current_number) + "次重连失败:" + str(ex))

    def Datalog(self, Data):
        date_time = datetime.now()  # 当前时间 格式为date
        currentData = datetime.today()  # 当前天  格式为date

        str_now_day = date_time.strftime("%Y-%m-%d")  # 当前天数 格式为str
        str_now_time = date_time.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间 格式为str

        current_path = os.getcwd()
        path = current_path + "\\DataLog\\Snap7Log"  # 文件夹路径

        if not os.path.exists(path):  # 如果该路径不存在
            os.makedirs(path)  # 创建一个路径

        if self.MaxDaysEnable:
            files = os.listdir(path)  # 获取当前路径所有文件名
            for file in files:  # for循环所有文件名
                timestamp = os.path.getctime(path + '\\' + file)  # 获取文件的创建时间，格式float
                file_create_time = datetime.fromtimestamp(timestamp)  # 文件的创建时间格式转换为date
                delta = currentData - file_create_time  # 当前时间减去文件创建时间 格式为date
                days = delta.days  # 转为换int
                if days > self.MaxDays:  # 如果天数大于设置值
                    os.remove(path + '\\' + file)

        with open(path + '\\' + str_now_day + '.log', "a+", encoding='utf-8') as DDDDD1:
            DDDDD1.write(str_now_time + "   " + self.__PLC_IP + "   " + Data + "\n")

    def Close(self):
        """
        断开堆垛机PLC

        :return:
        """
        if self.IsOpen:
            self.SiemensPLC.disconnect()
            self.IsOpen = False
        return True

    # 获取任务号
    def GetNewTaskCode(self):
        """
        获取新的任务号

        :return: 任务号
        """
        with self.lock:
            if self.WcsTaskCode == 0:
                self.WcsTaskCode = random.randint(1, 30000)
            else:
                self.WcsTaskCode += 1
            if self.WcsTaskCode == 30000:
                self.WcsTaskCode = 1
            return self.WcsTaskCode

    # 赋值堆垛机任务号
    def WriteTaskCode(self, taskCode1: int, taskCode2: int):
        """
        将任务号赋值给全局变量

        :param taskCode1: 1号货叉任务号
        :param taskCode2: 2号货叉任务号
        :return:
        """
        with self.lock:
            self.taskCode1 = taskCode1
            self.taskCode2 = taskCode2

    # 赋值任务类型
    def WriteTaskType(self, taskType1: int, taskType2: int):
        """
        将任务类型赋值给全局变量

        :param taskType1: 1号货叉任务类型
        :param taskType2: 2号货叉任务类型
        :return:
        """
        with self.lock:
            if taskType1 not in self.TaskTypeList:
                raise CRNTaskError("任务类型错误")
            if taskType2 not in self.TaskTypeList:
                raise CRNTaskError("任务类型错误")
            self.taskType1 = taskType1
            self.taskType2 = taskType2

    # 赋值任务参数
    def WriteTaskParam(self, Type: int, Layer1: int, Col1: int, Dire1: int, Layer2=0, Col2=0, Dire2=0):
        """
        将任务参数赋值全局变量

        :param Type: 0取货；1放货
        :param Layer1: 1号货叉层
        :param Col1: 1号货叉列
        :param Dire1: 1号货叉排
        :param Layer2: 2号货叉层
        :param Col2: 2号货叉列
        :param Dire2: 2号货叉排
        :return:
        """
        with self.lock:
            if not (Dire1 in self.Dire_WMS_To_CRN[self.crnNo]):
                raise CRNTaskError("货叉1取货方向错误")
            if not (Dire2 in self.Dire_WMS_To_CRN[self.crnNo]):
                raise CRNTaskError("货叉2取货方向错误")
            Dire1 = self.Dire_WMS_To_CRN[self.crnNo][Dire1]
            Dire2 = self.Dire_WMS_To_CRN[self.crnNo][Dire2]

            if Type == 0:
                self.fork1_pick_layer = Layer1
                self.fork1_pick_col = Col1
                self.fork1_pick_dire = Dire1
                self.fork2_pick_layer = Layer2
                self.fork2_pick_col = Col2
                self.fork2_pick_dire = Dire2
            if Type == 1:
                self.fork1_release_layer = Layer1
                self.fork1_release_col = Col1
                self.fork1_release_dire = Dire1
                self.fork2_release_layer = Layer2
                self.fork2_release_col = Col2
                self.fork2_release_dire = Dire2

    # 批量写入
    def SendTask(self):
        """
        将数据批量写入PLC

        :return:
        """
        try:
            DBNo = 1001
            Start = 0
            Size = 28
            Data = "%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X" \
                   % (self.fork1_pick_layer, self.fork1_pick_col, self.fork1_pick_dire,
                      self.fork1_release_layer, self.fork1_release_col, self.fork1_release_dire,
                      self.fork2_pick_layer, self.fork2_pick_col, self.fork2_pick_dire,
                      self.fork2_release_layer, self.fork2_release_col, self.fork2_release_dire,
                      self.taskType1, self.taskType2, 0, self.taskCode1, self.taskCode2, )
            Result = self.WriteDB(DBNo, Start, Data)
            if Result[0] != 1:
                raise CRNWriteDataError("写数据失败")
        except Exception as ex:
            raise ex

    # 驱动执行
    def ExecuteTask(self, Fork: int):
        """
        触发货叉执行

        :param Fork: 触发类型 1-1号货叉；2-2号货叉；3-先1后2；4-先2后1；
        :return:
        """
        try:
            if not (Fork in self.ForkTrigger):
                raise CRNTaskError("触发类型错误")
            self.__HeartBeatThread()
            if not self.online:
                raise CRNWarningException("堆垛机处于脱机状态！")
            self.fork_trigger = Fork
            DBNo = 1001
            Start = 28
            Size = 6
            Result = self.WriteDBInt(DBNo, Start, Fork)
            if Result[0] != 1:
                raise CRNWriteDataError("写触发失败")
        except Exception as ex:
            raise ex

    # 清除报警
    def ClearWarning(self):
        """
        清除堆垛机报警

        :return:
        """
        try:
            DBNo = 1001
            Start = 0
            Size = 34
            self.WriteDBInt(1001, 28, 0)
            time.sleep(self.__PulseWidth)
            Result = self.WriteDB(DBNo, Start, "%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X%04X"
                                  % (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 5, 0, 0))
            time.sleep(self.__PulseWidth)
            self.WriteDBInt(1001, 28, 0)
            if Result[0] != 1:
                raise CRNWriteDataError("写清除报警失败")
        except Exception as ex:
            raise ex

    # 获取堆垛机报警代码
    def GetWarnCode(self):
        """
        获取堆垛机报警代码

        :return: 堆垛机故代码
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                Result = self.error_code
            return Result
        except Exception as ex:
            raise ex

    # 获取堆垛机报警信息
    def GetWarning(self):
        """
        获取堆垛机报警文本

        :return: 报警内容
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                Status = self.state
                CrnCode = self.error_code
                Code1 = self.x_error_code
                Code2 = self.x_warn_code
                Code3 = self.y_error_code
                Code4 = self.y_warn_code
                Code5 = self.fork1_error_code
                Code6 = self.fork1_warn_code
                Code7 = self.fork2_error_code
                Code8 = self.fork1_warn_code
                x = self.x_real_position
                y = self.y_real_position
                fork1 = self.fork1_real_position
                fork2 = self.fork2_real_position
            msg = ""
            if Status in self.CRNErrorStateList:
                msg += self.CRNErrorStateList[Status]
            if Status == 1:
                if self.CRNWarning.__contains__(CrnCode):
                    msg += self.CRNWarning[CrnCode]
                    if CrnCode == 64:
                        msg += " 故障代码 %s 报警代码 %s 位置 %s" % (Code1, Code2, x)
                    if CrnCode == 65:
                        msg += " 故障代码 %s 报警代码 %s 位置 %s " % (Code3, Code4, y)
                    if CrnCode == 66:
                        msg += " 故障代码 %s 报警代码 %s 位置 %s " % (Code5, Code6, fork1)
                    if CrnCode == 67:
                        msg += " 故障代码 %s 报警代码 %s 位置 %s " % (Code7, Code8, fork2)
                else:
                    msg += "未知的错误代码 %s" % CrnCode
            if msg != "":
                raise CRNWarningException(msg)
        except Exception as ex:
            raise ex

    # 获取堆垛机状态
    def GetCRNState(self):
        """
        获取堆垛机设备状态

        :return: 1报警；2空闲；3忙碌；4手动；5强制手动
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                if not self.online:
                    raise CRNWarningException("堆垛机处于脱机状态！")
                Result = self.state
                if Result == 4:
                    raise CRNWarningException("堆垛机处于手动状态！")
                if Result == 5:
                    raise CRNWarningException("堆垛机处于强制手动状态！")
            # if self.CRNErrorStateList.__contains__(Result):
            #     raise CRNWarningException(self.CRNErrorStateList[Result])
            return Result
        except Exception as ex:
            raise ex

    # 获取堆垛机步骤
    def GetCRNStep(self, Fork: int):
        """
        获取堆垛机货叉任务步骤

        :param Fork: 货叉编号
        :return:
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                rlt = self.fork1_task_step, self.fork2_task_step
            return rlt[Fork - 1]
        except Exception as ex:
            raise ex

    # 获取堆垛机的货叉占位
    def GetForkFull(self, Fork: int):
        """
        获取堆垛机货叉占位信号

        :param Fork: 货叉编号
        :return: 1无货 2有货
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                rlt = self.fork1_occupy, self.fork2_occupy
            return rlt[Fork - 1]
        except Exception as ex:
            raise ex

    # 获取堆垛机的外侧探货光电状态
    def GetStorehouseState(self, Fork: int):
        """
        获取堆垛机探货光电占位

        :param Fork: 货叉编号
        :return:
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                rlt = self.fork1_storge_outside_occupy, self.fork2_storge_outside_occupy
            return rlt[Fork - 1]
        except Exception as ex:
            raise ex

    # 获取堆垛机的内侧探货光电状态
    def GetStorehouseStateInside(self, Fork: int):
        """
        1-左库位占位  2-右库位占位  3-左右库位占位

        :param Fork: 货叉编号
        :return:
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                rlt = self.fork1_storge_inside_occupy, self.fork2_storge_inside_occupy
            return rlt[Fork - 1]
        except Exception as ex:
            raise ex

    # 确认堆垛机探货光电
    def CheckStorehouseState(self, F: int, Fork: int, crnNo: int):
        """
        确认堆垛机探货光电

        :param F: 排号
        :param Fork: 货叉编号
        :param crnNo: 堆垛机编号
        :return:
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            Direction = self.Dire_WMS_To_CRN[crnNo][F]
            self.__HeartBeatThread()
            with self.lock:
                if Direction in (1, 2):
                    rlt = self.fork1_storge_outside_occupy, self.fork2_storge_outside_occupy
                    return rlt[Fork - 1] & Direction == Direction
                if Direction in (3, 4):
                    rlt = self.fork1_storge_inside_occupy, self.fork2_storge_inside_occupy
                    return rlt[Fork - 1] & (Direction - 2) == (Direction - 2)
        except Exception as ex:
            raise ex

    # 获取堆垛机的货叉是否中位
    def CheckForkSafe(self):
        """
        确认堆垛机货叉已回中

        :return:
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                # if abs(float(self.fork1_real_position)) > 5:
                #     raise CRNWarningException("货叉1不在中位，禁止执行任务！")
                if not self.fork1_middle:
                    raise CRNWarningException("货叉1不在中位，禁止执行任务！")
                if self.ForkNumber > 1:
                    # if abs(float(self.fork2_real_position)) > 5:
                    #     raise CRNWarningException("货叉2不在中位，禁止执行任务！")
                    if not self.fork2_middle:
                        raise CRNWarningException("货叉2不在中位，禁止执行任务！")
        except Exception as ex:
            raise ex

    # 获取堆垛机是否联机
    def CheckCRNAuto(self):
        """
        确认堆垛机处于联机状态

        :return:
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                if not self.online:
                    raise CRNWarningException("堆垛机处于脱机状态！")
        except Exception as ex:
            raise ex

    # 获取堆垛机是否完成任务
    def CheckCRNFinishTask(self, flag: int, fork: int, taskcode: str, maxRead: int):
        """
        确认堆垛机已完成任务

        :param flag: 0取货；1放货
        :param fork: 货叉编号
        :param taskcode: 需校验的任务号
        :param maxRead: 最大等待次数
        :return:
        """
        try:
            if fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                if not self.online:
                    raise CRNWarningException("堆垛机处于脱机状态！")
            state = self.state
            taskstep = self.fork1_task_step if fork == 1 else self.fork2_task_step
            finish_taskcode = self.fork1_finish_taskCode if fork == 1 else self.fork2_finish_taskCode
            if state == 3:  # 状态忙碌
                if maxRead < self.CurrentRead:
                    self.CurrentRead += 1
                    code, msg = -1, "堆垛机正在执行任务"
                else:
                    code, msg = 0, "堆垛机执行任务超时,请确认超时原因"
            elif state == 2:  # 状态空闲
                if finish_taskcode == taskcode and taskstep == (5 if flag == 0 else 9):
                    code, msg = 1, "2"
                elif finish_taskcode == taskcode:
                    code, msg = 0, "堆垛机任务步骤错误%s" % taskstep
                else:
                    code, msg = 0, "堆垛机完成任务号不一致%s" % finish_taskcode
            elif state == 1:  # 状态报警
                code, msg = 1, "1"
            else:
                code, msg = 0, self.CRNErrorStateList[state]
            if code != -1:
                self.CurrentRead = 0
            return code, msg
        except Exception as ex:
            raise ex

    # 扫码NG
    def ScanWarning(self):
        """
        扫码失败

        :return:
        """
        try:
            DBNo = 1001
            Start = 34
            Bit = 1
            Data = 1
            Result = self.WriteDBBit(DBNo, Start, Bit, Data)
            if Result[0] != 1:
                raise CRNWriteDataError(Result[1])
        except Exception as ex:
            raise ex

    # 获取堆垛机当前位置(激光测距)
    def GetCRNLocation(self):
        """
        获取堆垛机位置

        :return:
        """
        try:
            self.__HeartBeatThread()
            with self.lock:
                data1 = self.x_real_position
                data2 = self.y_real_position
                data3 = self.fork1_real_position
                data4 = self.fork2_real_position
            if self.ForkNumber > 1:
                return "行走%s 提升%s 1货叉%s 2货叉%s" % (data1, data2, data3, data4)
            return "行走%s 提升%s 1货叉%s" % (data1, data2, data3)
        except Exception as ex:
            raise ex

    # 获取堆垛机当前坐标
    def GetCRNCoordinate(self, Fork: int):
        """
        获取堆垛机坐标位置

        :param Fork: 货叉编号
        :return: 层，列
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                if Fork == 1:
                    Layer = self.fork1_layer
                    Col = self.fork1_col
                else:
                    Layer = self.fork2_layer
                    Col = self.fork2_col
            return Layer, Col
        except Exception as ex:
            raise ex

    # 获取条码
    def GetCRNBarCode(self, Fork: int):
        """
        获取堆垛机上货物条码

        :param Fork: 货叉编号
        :return: 货物条码
        """
        try:
            if Fork > self.ForkNumber:
                raise CRNTaskError("货叉总数量小于传参")
            self.__HeartBeatThread()
            with self.lock:
                if Fork == 1:
                    barcode = self.ReadDBString(1000, 86, 102)
                else:
                    barcode = self.ReadDBString(1000, 188, 102)
            return barcode
        except Exception as ex:
            raise ex

    def WriteDB(self, DBNumber: int, nStartAddr: int, Data: str) -> tuple:
        try:
            self.ReOpen()
            Data1 = SiemensDevice.StrToHex(Data)
            Val = bytearray(Data1)
            self.SiemensPLC.write_area(snap7.types.Areas.DB, DBNumber, nStartAddr, Val)
            rel = self.ReadDB(DBNumber, nStartAddr, int(len(Data)/2))
            if rel[1].upper() != Data:
                return -1, "写入失败"
            return 1, "1"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDB(self, DBNumber: int, nStart: int, nAmout: int) -> tuple:
        try:
            self.ReOpen()
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            Data = binascii.b2a_hex(Data)
            Data = Data.decode("utf-8")
            return 1, Data
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDBbytearray(self, DBNumber: int, nStart: int, nAmout: int):
        try:
            self.ReOpen()
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            return 1, Data
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDBBit(self, DBNumber: int, nPort: int, nBit: int):
        try:
            self.ReOpen()
            Data = self.SiemensPLC.read_bit(snap7.types.S7AreaDB, DBNumber, nPort * 8 + nBit)
            if Data[0] == 1:
                return 1, "1"
            return 1, "0"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDBFloat(self, DBNumber: int, nStart: int) -> tuple:
        try:
            self.ReOpen()
            nAmout = 4
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            aaa = struct.unpack("!f", Data)
            return 1, "%.3f" % struct.unpack("!f", Data)[0]
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDBInt(self, DBNumber: int, nStart: int) -> tuple:
        try:
            self.ReOpen()
            nAmout = 2
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            Data = binascii.b2a_hex(Data)
            return 1, int(Data, 16)
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def WriteDBFloat(self, DBNumber: int, nStartAddr: int, Data: int) -> tuple:
        try:
            self.ReOpen()
            Data = struct.pack('>f', Data)
            Val = bytearray(Data)
            self.SiemensPLC.write_area(snap7.types.Areas.DB, DBNumber, nStartAddr, Val)
            return 1, "1"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def WriteDBInt(self, DBNumber: int, nStartAddr: int, Data: int) -> tuple:
        try:
            self.ReOpen()
            Data1 = '%04X' % Data
            Data1 = SiemensDevice.StrToHex(Data1)
            Val = bytearray(Data1)
            self.SiemensPLC.write_area(snap7.types.Areas.DB, DBNumber, nStartAddr, Val)
            rel = self.ReadDBInt(DBNumber,nStartAddr)
            if int(rel[1]) != Data:
                return -1, "写入失败"
            return 1, "1"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def WriteDBBit(self, DBNumber: int, Port: int, Bit: int, Data: int) -> tuple:
        try:
            self.ReOpen()
            Start = Port * 8 + Bit
            self.SiemensPLC.write_bit(snap7.types.S7AreaDB, DBNumber, Start, Data)
            rel = self.ReadDBBit(DBNumber,Port,Bit)
            if int(rel[1]) != Data:
                return -1, "写入失败"
            return 1, "1"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def ReadDBString(self, DBNumber: int, nStart: int, nAmout: int) -> tuple:
        try:
            self.ReOpen()
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            # aa = 2 + ord(Data[1:2])
            Result = Data.decode("utf-8")[2:2 + ord(Data[1:2])].replace("\x00", "").replace(" ", "")
            if Result == "":
                return 1, "NULL"
            return 1, Result
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex

    def WriteDBString(self, DBNumber: int, nStart: int, Data: str) -> tuple:
        try:
            self.ReOpen()
            data3 = chr(len(Data)) + Data
            Val = bytearray(data3, "utf-8")
            self.SiemensPLC.write_area(snap7.types.Areas.DB, DBNumber, nStart + 1, Val)
            rel = self.ReadDBString(DBNumber, nStart, len(Data) + 2)
            if rel != Data:
                raise CRNCommError("写入失败")
            return 1, "1"
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex


    def ReadP_FUidData(self, DBNumber: int, nStart: int, nAmout: int):
        try:
            self.ReOpen()
            Data = self.SiemensPLC.read_area(snap7.types.Areas.DB, DBNumber, nStart, nAmout)
            Data = Data[2:]
            Data = bytes(Data)
            Data = binascii.b2a_hex(Data)
            Data = Data.upper().decode("utf-8")[0:16]
            return (1, Data)
        # except Snap7Exception as ex:
        #     self.IsOpen = False
        #     raise CRNCommError(str(ex))
        except Exception as ex:
            raise ex


# Debug
if __name__ == '__main__':
    SiemensDevice = SiemensDevice()
    try:
     #    SiemensDevice.strTobytearray("0023")
        print(SiemensDevice.Open("192.168.1.163", 0, 0))
        # print(SiemensDevice.GetCRNLocation())
        # aa = SiemensDevice.ReadDB(1000,0,8)
        # bb = SiemensDevice.strTobytearray(aa[1])
        # # dd = aa[1]
        # # ee = dd[0:4]
        # cc = SiemensDevice.strToFloat(aa[1][8:16])
        # print(aa,bb,cc)
        # print(SiemensDevice.GetWarning())
        # print(SiemensDevice.GetForkFull())
        # print(SiemensDevice.WriteTaskType(9, 0))
        # print(SiemensDevice.WriteTaskParam(0, 1001, 1001, 1, 0, 0, 0))  # 取货坐标
        # print(SiemensDevice.WriteTaskParam(1, 1, 1, 1, 0, 0, 0))  # 放货坐标
        # print(SiemensDevice.WriteTaskCode(SiemensDevice.GetNewTaskCode(), 0))  # 写任务号
        # print(SiemensDevice.SendTask())
        # print(SiemensDevice.ExecuteTask(1))
        # print(SiemensDevice.ReOpen())
        # print(SiemensDevice.GetState())
        # print(SiemensDevice.GetWarning())
        # print(SiemensDevice.GetForkFull())
        # print(SiemensDevice.GetStorehouseState())
        # time.sleep(30000)
        # print(SiemensDevice.CheckForkSafe())
        # SiemensDevice.WriteDB(1,0,"014D01C3")
        # print(SiemensDevice.ReadDB(1,0,4))
        # SiemensDevice.WriteDBString(200, 564, "")
        # print(SiemensDevice.ReadDBString(200, 564, 100))
    except Exception as ex:
        print(str(ex))
