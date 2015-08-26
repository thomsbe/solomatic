class MsgTemp:
    def __init__(self, temp):
        self.temp = temp
        self.type = "fhem.temp.read"
        self.source = "fhem.reader"
        self.device = "script"
