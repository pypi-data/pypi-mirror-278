from .datatypes import Group, DecodedGroup, \
    GroupIdentifier, PSDetails, \
    RTDetails, PINSLCetails, \
    PTYNDetails, CTDetails, \
    TDCDetails, InHouseDetails, \
    ODAAidDetails, EONBDetails, \
    EONADetails, ODADetails, \
    LongPSDetails, FastSwitchingInformation, \
    Details

from .charset import RDSCharsetDecode
from .comfort import BitManipulator
from .af import AF_Codes, AlternativeFrequencyEntryDecoded

class GroupDecoder:
    @staticmethod
    def decode(group:Group):
        def readValue(val, bits, index,max=16):
            return BitManipulator.get_bits(val,bits,index,max)
        def readGroup():
            return readValue(group.b,4,0), BitManipulator.get_bit(group.b, 4)
        def readTP():
            return bool(BitManipulator.get_bit(group.b,5))
        def readPTY():
            return readValue(group.b, 5, 6)
        group_number, group_version = readGroup()
        group_out = DecodedGroup(group,group.a,readTP(),readPTY(), GroupIdentifier(group_number, bool(group_version)), Details())
        
        def decode_group_0():
            def readTAMS():
                return bool(BitManipulator.get_bit(group.b,11)), bool(BitManipulator.get_bit(group.b,12))
            def readSegment():
                is_di = bool(BitManipulator.get_bit(group.b,13))
                return is_di, readValue(group.b, 2, 14)
            def decodeAF():
                af0 = (group.c >> 8) & 0xff
                af1 = group.c & 0xff
                entry = AlternativeFrequencyEntryDecoded(None,None,None,None,None)
                if af0 == AF_Codes.NoAF.value and af1 == AF_Codes.Filler.value:
                    entry.is_af = False
                elif af0 == AF_Codes.LfMf_Follows.value and af1 == AF_Codes.Filler.value:
                    entry.lfmf_follows = True
                elif BitManipulator.get_bits(af0, 3, 0, 8) == 7:
                    entry.all_af_lenght = (af0-AF_Codes.NumAFSBase.value)
                elif af0 != AF_Codes.LfMf_Follows.value and af0 != AF_Codes.NoAF.value:
                    entry.af_freq = af0
                    if af1 != AF_Codes.Filler.value:
                        entry.af_freq1 = af1
                return entry
                
            ta, ms = readTAMS()
            is_di, segment = readSegment()
            if group_version == 0:
                af_entry = decodeAF()
            else:
                af_entry = None
            det = PSDetails(segment,None,None,None,None,ms,ta,"",af_entry)
            #i've spent a long time understanding di, and to be honest when i understand it, its fucking genius (from redsea's source code)
            match segment:
                case 0:
                    det.di_dpty = is_di
                case 1:
                    det.di_compressed = is_di
                case 2:
                    det.di_artificial_head = is_di
                case 3:
                    det.di_stereo = is_di
            char_0 = (group.d >> 8) & 0xFF
            char_1 = group.d & 0xFF
            det.text += RDSCharsetDecode.translate(char_0)
            det.text += RDSCharsetDecode.translate(char_1)
            group_out.details = det
        def decode_group_2():
            def readABSegment():
                return bool(BitManipulator.get_bit(group.b,11)), readValue(group.b, 4, 12)
            ab, segment = readABSegment()
            det = RTDetails(segment,ab,"")
            if not group_out.group.group_version == 1:
                char_1 = (group.c >> 8) & 0xFF
                char_2 = group.c & 0xFF
                char_3 = (group.d >> 8) & 0xFF
                char_4 = group.d & 0xFF
                det.text += RDSCharsetDecode.translate(char_1)
                det.text += RDSCharsetDecode.translate(char_2)
                det.text += RDSCharsetDecode.translate(char_3)
                det.text += RDSCharsetDecode.translate(char_4)
            else:
                char_1 = (group.d >> 8) & 0xFF
                char_2 = group.d & 0xFF
                det.text += RDSCharsetDecode.translate(char_1)
                det.text += RDSCharsetDecode.translate(char_2)
            group_out.details = det
        def decode_group_1():
            det = PINSLCetails(((group.c & 0xfff) if group_version == 0 else None),None,None,None,None,None)
            if group_version == 0:
                det.variant_code = readValue(group.c,3,0,15)
                det.is_lic = (det.variant_code == 3)
            det.pin_day = readValue(group.d,5,0)
            det.pin_hour = readValue(group.d,5,5)
            det.pin_minute = readValue(group.d,6,10)
            group_out.details = det
        def decode_group_10():
            def readABSegment():
                return bool(BitManipulator.get_bit(group.b,11)), int(BitManipulator.get_bit(group.b,15))
            ab, segment = readABSegment()
            det = PTYNDetails(segment,ab,"")
            char_1 = (group.c >> 8) & 0xFF
            char_2 = group.c & 0xFF
            char_3 = (group.d >> 8) & 0xFF
            char_4 = group.d & 0xFF
            det.text += RDSCharsetDecode.translate(char_1)
            det.text += RDSCharsetDecode.translate(char_2)
            det.text += RDSCharsetDecode.translate(char_3)
            det.text += RDSCharsetDecode.translate(char_4)
            group_out.details = det
        def decode_group_4():
            mjd_buffer = "0b"
            mjd_buffer += str(BitManipulator.get_bit(group.b,14))
            mjd_buffer += str(BitManipulator.get_bit(group.b,15))
            mjd_buffer += bin(readValue(group.c,15,0)).removeprefix("0b")
            hour_buffer = "0b"
            hour_buffer += str(BitManipulator.get_bit(group.c,15))
            hour_buffer += bin(readValue(group.d,4,0)).removeprefix("0b")
            
            mjd = int(mjd_buffer,2)
            hour = int(hour_buffer,2)
            minute = readValue(group.d,6,4)
            time_sense = bool(BitManipulator.get_bit(group.d,10))
            time_diffence = readValue(group.d,5,11)
            group_out.details = CTDetails(mjd, hour, minute, time_sense, time_diffence)
        def decode_group_5():
            address = readValue(group.b,5,11)
            data = []
            if group_version == 0:
                data.append((group.c >> 8) & 0xFF)
                data.append((group.c & 0xFF))
            data.append((group.d >> 8) & 0xFF)
            data.append((group.d & 0xFF))
            group_out.details = TDCDetails(address, data)
        def decode_group_6():
            data_from_b = readValue(group.b,5,11)
            data = [data_from_b]
            if group_version == 0:
                data.append(group.c)
            data.append(group.d)
            group_out.details = InHouseDetails(data)
        def decode_group_3():
            group_number_odaaid = readValue(group.b, 4, 11)
            group_version_odaaid = bool(BitManipulator.get_bit(group.b,15))
            group_out.details = ODAAidDetails(GroupIdentifier(group_number_odaaid, group_version_odaaid), group.d, group.c)
        def decode_group_14():
            on_pi = group.d
            on_tp = bool(BitManipulator.get_bit(group.b,10))
            if group.is_version_b:
                on_ta = bool(BitManipulator.get_bit(group.b,11))
                group_out.details = EONBDetails(on_pi, on_tp, on_ta)
            else:
                variant_code = readValue(group.b,4,12)
                on_ps_segment, on_ps_text = None, ""
                on_af, on_pty, on_ta = None, None, None
                if variant_code < 4:
                    on_ps_segment = variant_code
                    char_1 = (group.c >> 8) & 0xFF
                    char_2 = group.c & 0xFF
                    on_ps_text += RDSCharsetDecode.translate(char_1)
                    on_ps_text += RDSCharsetDecode.translate(char_2)
                match variant_code:
                    case 4:
                        on_af = group.c
                    case 13:
                        on_pty = readValue(group.c,5,0)
                        on_ta = bool(BitManipulator.get_bit(group.c,15))
                group_out.details = EONADetails(on_pi, on_tp, on_ta, on_ps_segment, on_ps_text, on_pty, on_af, variant_code)
        def decode_group_15():
            if group_version == 0: #15A
                #LPS
                segment = readValue(group.b, 4, 12)
                det = LongPSDetails(segment,"")
                char_1 = (group.c >> 8) & 0xFF
                char_2 = group.c & 0xFF
                char_3 = (group.d >> 8) & 0xFF
                char_4 = group.d & 0xFF
                det.text += RDSCharsetDecode.translate(char_1)
                det.text += RDSCharsetDecode.translate(char_2)
                det.text += RDSCharsetDecode.translate(char_3)
                det.text += RDSCharsetDecode.translate(char_4)
                group_out.details = det
            elif group_version == 1: #15B
                def readTAMS():
                    return bool(BitManipulator.get_bit(group.b,11)), bool(BitManipulator.get_bit(group.b,12))
                def readSegment():
                    is_di = bool(BitManipulator.get_bit(group.b,13))
                    return is_di, readValue(group.b, 2, 14)
                ta, ms = readTAMS()
                is_di, segment = readSegment()
                det = FastSwitchingInformation(segment,None,None,None,None,ms,ta)
                match segment:
                    case 0:
                        det.di_dpty = is_di
                    case 1:
                        det.di_compressed = is_di
                    case 2:
                        det.di_artificial_head = is_di
                    case 3:
                        det.di_stereo = is_di
                group_out.details = det
        def decode_group_oda():
            #same as inhouse
            data_from_b = readValue(group.b,5,11)
            data = [data_from_b]
            if group_version == 0:
                data.append(group.c)
            data.append(group.d)
            group_out.details = ODADetails(data)
            

        match group_number:
            case 0:
                decode_group_0()
            case 1:
                decode_group_1()
            case 2:
                decode_group_2()
            case 3:
                if group_version == 0: decode_group_3()
                else: decode_group_oda()
            case 4:
                if group_version == 0: decode_group_4()
                else: decode_group_oda()
            case 5:
                decode_group_5()
            case 6:
                decode_group_6()
            case 10:
                if group_version == 0: decode_group_10()
                else: decode_group_oda()
            case 14:
                decode_group_14()
            case 15:
                decode_group_15()
            case _:
                decode_group_oda()
        return group_out