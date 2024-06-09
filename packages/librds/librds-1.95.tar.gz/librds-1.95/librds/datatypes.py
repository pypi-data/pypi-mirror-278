from dataclasses import dataclass
from .af import AlternativeFrequencyEntryDecoded

@dataclass
class Group:
    """This is a basic group function to store the blocks"""
    a:int
    b:int
    c:int
    d:int
    is_version_b: bool
    def to_list(self):
        return [self.a, self.b, self.c, self.d]
    def __iter__(self):
        return self.to_list()

@dataclass
class GroupIdentifier:
    group_number: int
    group_version: bool


@dataclass
class Details:
    details=True

@dataclass
class PSDetails(Details):
    segment: int
    di_stereo:bool
    di_artificial_head:bool
    di_compressed:bool
    di_dpty:bool
    ms: bool
    ta: bool
    text: str
    af: AlternativeFrequencyEntryDecoded

@dataclass
class FastSwitchingInformation(Details):
    segment: int
    di_stereo:bool
    di_artificial_head:bool
    di_compressed:bool
    di_dpty:bool
    ms: bool
    ta: bool

@dataclass
class RTDetails(Details):
    segment: int
    ab: bool
    text: str

@dataclass
class LongPSDetails(Details):
    segment: int
    text: str

@dataclass
class PTYNDetails(Details):
    segment: int
    ab: bool
    text: str

@dataclass
class PINSLCetails(Details):
    data:int
    is_lic:bool
    variant_code: int
    pin_day: int
    pin_hour: int
    pin_minute: int

@dataclass
class CTDetails(Details):
    mjd: int
    hour: int
    minute: int
    time_sense: bool
    local_offset: int

@dataclass
class TDCDetails(Details):
    channel: int
    data: list[int]

@dataclass
class InHouseDetails(Details):
    data: list[int]

@dataclass
class ODADetails(Details):
    data: list[int]

@dataclass
class ODAAidDetails(Details):
    oda_group: GroupIdentifier
    aid:int
    scb:int

@dataclass
class EONBDetails(Details):
    pi: int
    tp: bool
    ta: bool

@dataclass
class EONADetails(Details):
    pi: int
    tp: bool
    ta: bool
    ps_segment:int
    ps_text:str
    pty: int
    on_af: int
    variant_code:int

@dataclass
class DecodedGroup:
    raw_group:Group
    pi: int
    tp: bool
    pty: int
    group: GroupIdentifier
    details:Details