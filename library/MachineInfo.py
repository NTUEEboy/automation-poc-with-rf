import wmi


class MachineInfo:
    def __init__(self):
        self._computer = wmi.WMI()

    def computer_info(self):
        return self._computer.Win32_ComputerSystem()[0].Caption

    def gpu_info(self):
        return self._computer.Win32_VideoController()[0].Caption
