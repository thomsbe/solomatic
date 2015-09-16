class MsgClima:
    def __init__(self, temp, hum):
        self.temp = temp
        self.hum = hum
        self.type = "fhem.temp.read"
        self.source = "fhem.reader"
        self.device = "script"


class MsgNfc:
    def __init__(self, uuid):
        self.uuid = uuid
        self.type = "nfc.uuid.read"
        self.source = "nfc.reader"
        self.device = "pi"
