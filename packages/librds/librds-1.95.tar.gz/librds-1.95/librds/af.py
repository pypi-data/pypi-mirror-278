from enum import Enum, IntEnum
from dataclasses import dataclass

class AF_Codes(Enum):
    Filler = 0xCD
    NoAF = 0xE0
    NumAFSBase = 0xE0 #same as no af
    LfMf_Follows = 0xFA
class AF_Bands(Enum):
    FM = 0
    LF = 1
    MF = 2
    MF_RBDS = 3
class AlternativeFrequencyEntry:
    """This is a AF Entry which will be used by the AF Class"""
    af_freq = 0
    lenght = 1
    lfmf = False
    freq = 0.0
    def __init__(self, band:IntEnum, frequency:float) -> None:
        self.freq = frequency
        self.band = band
        self.lfmf = band != AF_Bands.FM
        self.lenght = 2 if self.lfmf else 1
        match band:
            case AF_Bands.FM:
                self.af_freq = int((int(frequency*10)) - (87.5*10))
            case AF_Bands.LF:
                self.af_freq = int(int(frequency - 153.0)/9+1)
            case AF_Bands.MF:
                self.af_freq = int(int(frequency - 531.0)/9+16)
            case AF_Bands.MF_RBDS:
                self.af_freq = int(int(frequency - 540.0)/10+17)
    def __len__(self):
        return self.lenght
    def __repr__(self) -> str:
        return f"<AFEntry freq={self.freq} band={self.band.name} af_freq={self.af_freq} len={self.lenght} lfmf={self.lfmf}>"
class AlternativeFrequency:
    """This is a working Alterntive Frequency implementation that was tested on FM, LF, MF, RBDS MF
    however the rbds MF does have a problem, on rds mf 540 and 549 work but 550 doesnt, this is expected as 550 is not divisible by 9 as in europe am has a 9 khz step
    in the us however am has a 10 khz step 540 works as expected but 549 round to 540, as expected but 550 does the same?
    but im doing rbds out of generosity, not need or want"""
    def __init__(self, af:list[AlternativeFrequencyEntry]=[]) -> None:
        self.af = af
        self.cur_idx = 0
    def get_no_af(self=None): return AF_Codes.NoAF.value << 8 | AF_Codes.Filler.value
    def get_lfmf_follows(self=None): return AF_Codes.LfMf_Follows.value << 8 | AF_Codes.Filler.value
    def get_next(self):
        print(self.cur_idx)
        if len(self.af) > 25:
            raise Exception("Too much afs!")
        if len(self.af) > self.cur_idx or len(self.af) > 0:
            out = 0
            if self.cur_idx == 0:
                if self.af[self.cur_idx].lfmf: print("AM can't be the first AF")
                self.cur_idx += 1
                return (AF_Codes.NumAFSBase.value + len(self.af)) << 8 | self.af[0].af_freq
            else:
                try:
                    if not self.af[self.cur_idx-1].lfmf:
                        out = self.af[self.cur_idx-1].af_freq << 8
                    else:
                        out = AF_Codes.LfMf_Follows.value << 8
                except IndexError:
                    if not len(self.af) == 1:
                        self.cur_idx = 0
                        return self.get_next()
                    else:
                        out = self.af[0].af_freq << 8
                try:
                    if not self.af[self.cur_idx].lfmf:
                        try:
                            if self.af[self.cur_idx]:
                                out |= self.af[self.cur_idx].af_freq
                        except IndexError:
                            out |= AF_Codes.Filler.value
                    else:
                            out |= self.af[self.cur_idx].af_freq
                except IndexError:
                    if self.cur_idx == 1 and len(self.af) == 1:
                        out |= AF_Codes.Filler.value
                self.cur_idx += 2
                if self.cur_idx >= len(self.af): self.cur_idx = 0
                return out
        else:
            self.cur_idx = 0
            return self.get_no_af()
@dataclass
class AlternativeFrequencyEntryDecoded:
    is_af:bool
    af_freq:int
    af_freq1:int
    lfmf_follows:bool
    all_af_lenght:int