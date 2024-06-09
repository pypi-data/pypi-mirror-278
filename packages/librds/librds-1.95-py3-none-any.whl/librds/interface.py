class GroupInterface:
    @staticmethod
    def getPS(text: str):
        if len(text) > 8: text = text[:8]
        return text.ljust(8), 4
    @staticmethod
    def getRT(text: str,full:bool=False):
        if len(text) >= 64: text = text[:64]
        elif not full: text += "\r" # http://www.interactive-radio-system.com/docs/EN50067_RDS_Standard.pdf page 26
        if not full:
            while len(text) % 4: # if we don't have text to equally spread across 4 charcter parts then we add padding
                text = text + " "
            segments = 0.0
            for _ in range(len(text)):
                segments = segments + 0.25 # 1/4 = 0.25 | 0.25*4 = 1
            if not float(segments).is_integer(): raise Exception("Segment error (segment is not int)")
            if int(segments) > 16: return None, None
            return text, int(segments)
        else:
            return text.ljust(64), 16
    @staticmethod
    def getLongPS(text: str,full:bool=False):
        if len(text) >= 32: text = text[:32]
        elif not full: text += "\r"
        if not full:
            while len(text) % 4:
                text = text + " "
            segments = 0.0
            for _ in range(len(text)):
                segments = segments + 0.25
            if not float(segments).is_integer(): raise Exception("Segment error (segment is not int)")
            if int(segments) > 8: return None, None
            return text, int(segments)
        else:
            return text.ljust(32), 8
    @staticmethod
    def getPTYN(text: str):
        if len(text) > 8: text = text[:8]
        return text.ljust(8), 2