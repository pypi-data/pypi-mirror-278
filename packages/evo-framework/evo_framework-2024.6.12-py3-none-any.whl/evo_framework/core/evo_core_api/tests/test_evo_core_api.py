import unittest
import sys
import os
import lz4
import json
import gzip
import time
import io
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path + "/../../../../../")

from evo.evo_framework import *
from evo.evo_framework.core.evo_core_api.entity.evo_core_api_entity_pb2 import *

import enum
import struct
import io

from cyborgai_py import *

IuLog.doSetLevel("INFO")
def my_callback(number, text):
    print(f"Callback called from Rust with number {number} and text '{text}'")

class TestAction(unittest.IsolatedAsyncioTestCase):
     
    async def asyncSetUp(self):
        self.COUNT_TEST = int(1e6)
        IuLog.doInfo(__name__,f"COUNT_TEST: {self.COUNT_TEST} ")
    

    async def test_0_OnRequestRust(self): 
        start_time = time.time() 
        totalByte = 0
        
       # print(eApiActionInput)

        for i in range(self.COUNT_TEST):
            
            idRequest, dataRequest = to_request(b'data')
            
            '''
            dataDecompressed = lz4.frame.decompress(dataRequest)
            eRequest:ERequest = IuApi.toEObject(ERequest(),dataDecompressed)
            
            print("eRequest:",eRequest)
            print("eRequest.data:",eRequest.data)
            
            if isinstance(eRequest, ERequest):
                if (len(eRequest.id) < 64):
                    raise Exception(f"NOT_VALID_ID_{eRequest.id}")
                
                hash = IuCryptHash.toSha256Bytes(eRequest.data)
               
                
                IuLog.doInfo(__name__,f"CHUNK HASH: {hash.hex()} hash:{ eRequest.hash.hex()} { eRequest.hash==hash}")
                
                #IuLog.doInfo(__name__,f"CHUNK HASH: {eRequest.chunk} {hash!r} hash:{ eRequest.hash!r} { eRequest.hash==hash}")
                if hash !=  eRequest.hash:
                    raise Exception(f"NOT_VALID_HASH_{ eRequest.hash.hex()}")
                
                if not eRequest.pk:
                    raise Exception("NOT_VALID_PK")
                IuLog.doVerbose(__name__,f"checkSign: {eRequest}")
                #signSha256 = IuCryptHash.toSha256Bytes(eRequest.id.encode() + hash)
                signSha256 = IuCryptHash.toSha256Bytes( hash)
                isValid = IuCryptEC.verify_data(eRequest.hash, eRequest.sign, eRequest.pk)
                IuLog.doVerbose(__name__,f"checkSign: {eRequest.id} {signSha256!r} isValid:{isValid}")
                if not isValid:
                        raise Exception("NOT_VALID_SIGN")
            '''
            self.assertIsNotNone(idRequest)
            self.assertIsNotNone(dataRequest)
          #  self.assertEqual(eApiActionInput.mapEApiTypePb.map[eApiType0.id].data,eApiActionOut.mapEApiTypePb.map[eApiType0.id].data)
               
        endTime = time.time() - start_time    
        IuLog.doInfo(__name__,f"test_0_OnRequestRust time: {str(endTime)} avg: {endTime/self.COUNT_TEST} totalByte: {totalByte} bytes: {totalByte/self.COUNT_TEST}")
    
    async def Atest_0_OnRequestPython(self): 
        start_time = time.time() 
        totalByte = 0
        CApiFlow.getInstance().doInit(True)
       # print(eApiActionInput)

        for i in range(self.COUNT_TEST):
            
            dataRequest = await CApiFlow.getInstance().onResponse("idRequest", b'data')
          
           
            self.assertIsNotNone(dataRequest)
          #  self.assertEqual(eApiActionInput.mapEApiTypePb.map[eApiType0.id].data,eApiActionOut.mapEApiTypePb.map[eApiType0.id].data)
               
        endTime = time.time() - start_time    
        IuLog.doInfo(__name__,f"test_0_OnRequestPython time: {str(endTime)} avg: {endTime/self.COUNT_TEST} totalByte: {totalByte} bytes: {totalByte/self.COUNT_TEST}")
    
       
       
       

   # async def test_0_RustCallBack(self): 
    #    call_python_callback_with_params(my_callback, 42, "Hello from Rust")

    async def Atest_0_Serialization_EActionPy(self):  
     
        start_time = time.time() 
        totalByte = 0
        
       # print(eApiActionInput)

        for i in range(self.COUNT_TEST):
            
            eApiActionInput = EActionPy(
           # id=IuKey.generateId(),
           # time=IuKey.generateTime(), 
           # action="action",
        )
            eApiActionInput.id = IuKey.generateId()
            eApiActionInput.time=IuKey.generateTime()
            eApiActionInput.action="action"
        
            eApiActionInput.id = f"{i}"
            dataSerialize = eApiActionInput.to_bytes()
            totalByte += len(dataSerialize)
            eApiActionOut = EActionPy.from_bytes(dataSerialize)
          
            self.assertEqual(eApiActionInput.id, eApiActionOut.id)
          #  self.assertEqual(eApiActionInput.mapEApiTypePb.map[eApiType0.id].data,eApiActionOut.mapEApiTypePb.map[eApiType0.id].data)
               
        endTime = time.time() - start_time    
        IuLog.doInfo(__name__,f"test_0_Serialization_EActionPy time: {str(endTime)} avg: {endTime/self.COUNT_TEST} totalByte: {totalByte} bytes: {totalByte/self.COUNT_TEST}")
    
    async def Atest_0_SerializationEvo(self):  
      
        start_time = time.time() 
        totalByte= 0
        
        
       # print(eApiActionInput)
        
        for i in range(self.COUNT_TEST):
            
            eActionInput:EAction = IuApi.newEAction("do_action")       
            eActionInput.doSetInput(EnumApiType.STRING, "eApiType0", b"data_0",".png")
            
            dataSerialize = eActionInput.toBytes()
            #print("dataSerialize", dataSerialize)
            totalByte += len(dataSerialize)
            eActionOutput = EAction()
            eActionOutput = eActionOutput.fromBytes(dataSerialize)
 
            #print("\n\n",eActionOutput)
           
            self.assertEqual(eActionInput.id, eActionOutput.id)
           # self.assertEqual(eApiActionInput.mapEApiType.doGet(eApiType0.id).data, eApiActionOutput.mapEApiType.doGet(eApiType0.id).data)
                  
        endTime = time.time() - start_time
        IuLog.doInfo(__name__,f" test_SerializationEvo time:{str(endTime) }  avg:{endTime/self.COUNT_TEST} totalByte:{totalByte} bytes:{totalByte/self.COUNT_TEST} ")
        
    async def Atest_1_SerializationProtoBuff(self):  
     
        start_time = time.time() 
        totalByte = 0
        
        
        
       # print(eApiActionInput)

        for i in range(self.COUNT_TEST):
            
            eApiActionInput = EActionPb(
            id=IuKey.generateId(),
            time=IuKey.generateTime(), 
            version=1,  
            action="action",
           
            mapEActionItem = MapEActionItemPb()
        )
        
            eApiType0 = EActionItemPb(
                id="eApiType0",
                time=IuKey.generateTime(), 
                version=1,  
                enumApiType=EnumApiTypePb.TEXT, 
                isOutput=False, 
                isUrl=False, 
                typeExt=".png", 
                data=b"data_0" 
            )
    
            eApiActionInput.mapEActionItem.map[eApiType0.id].CopyFrom(eApiType0)
                
            
            eApiActionInput.id = f"{i}"
            dataSerialize = eApiActionInput.SerializeToString()
            totalByte += len(dataSerialize)
            eApiActionOut = EActionPb()
            eApiActionOut.ParseFromString(dataSerialize)
            self.assertEqual(eApiActionInput.id, eApiActionOut.id)
          #  self.assertEqual(eApiActionInput.mapEApiTypePb.map[eApiType0.id].data,eApiActionOut.mapEApiTypePb.map[eApiType0.id].data)
               
        endTime = time.time() - start_time    
        IuLog.doInfo(__name__,f"test_1_SerializationProtoBuff time: {str(endTime)} avg: {endTime/self.COUNT_TEST} totalByte: {totalByte} bytes: {totalByte/self.COUNT_TEST}")
    
    
    '''
    async def test_2_DeserializationEvoProto(self):  
        start_time = time.time() 
        dataSerialize= b'\n@5ADDFB1ECF1C0C9935E32B36CDE29DE0A9DCE52A1811299BF8493B844633965A\x10\xa6\xf6\x85\xef\xe212\x04sign:\x06do_rtc@\x01H\nz\xba!\n@5ADDFB1ECF1C0C9935E32B36CDE29DE0A9DCE52A1811299BF8493B844633965A\x10\x8f\xf6\x85\xef\xe21"@5ADDFB1ECF1C0C9935E32B36CDE29DE0A9DCE52A1811299BF8493B844633965A2\xac v=0\r\no=- 5334465520434695336 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0 1\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS c819fe8b-3bde-4b3f-98a3-4e30e38a7252\r\nm=video 65466 UDP/TLS/RTP/SAVPF 127 120 125 119 124 118 123 117 122 116 39 40 115 114 121\r\nc=IN IP4 172.20.10.10\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=candidate:3094488124 1 udp 2122194687 172.20.10.10 65466 typ host generation 0 network-id 1 network-cost 50\r\na=candidate:880941575 1 udp 2122262783 2a02:b127:13:d0b6:c4dd:f172:74ee:1a5b 55333 typ host generation 0 network-id 2 network-cost 50\r\na=ice-ufrag:R/Hd\r\na=ice-pwd:SaezVaNICQAaVRNYV9qHyWv9\r\na=ice-options:trickle\r\na=fingerprint:sha-256 56:19:EB:54:5A:A3:50:8B:5C:AE:5B:84:6C:EB:D2:16:EA:A0:01:6C:F2:5D:F3:21:4B:1F:F9:3C:F4:E8:FD:C8\r\na=setup:actpass\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:toffset\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 urn:3gpp:video-orientation\r\na=extmap:4 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=extmap:5 http://www.webrtc.org/experiments/rtp-hdrext/playout-delay\r\na=extmap:6 http://www.webrtc.org/experiments/rtp-hdrext/video-content-type\r\na=extmap:7 http://www.webrtc.org/experiments/rtp-hdrext/video-timing\r\na=extmap:8 http://www.webrtc.org/experiments/rtp-hdrext/color-space\r\na=extmap:9 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=extmap:10 urn:ietf:params:rtp-hdrext:sdes:rtp-stream-id\r\na=extmap:11 urn:ietf:params:rtp-hdrext:sdes:repaired-rtp-stream-id\r\na=sendrecv\r\na=msid:c819fe8b-3bde-4b3f-98a3-4e30e38a7252 8f6b6c2a-3c2d-43d5-887b-e0f684389f8a\r\na=rtcp-mux\r\na=rtcp-rsize\r\na=rtpmap:127 VP8/90000\r\na=rtcp-fb:127 goog-remb\r\na=rtcp-fb:127 transport-cc\r\na=rtcp-fb:127 ccm fir\r\na=rtcp-fb:127 nack\r\na=rtcp-fb:127 nack pli\r\na=fmtp:127 implementation_name=Internal\r\na=rtpmap:120 rtx/90000\r\na=fmtp:120 apt=127\r\na=rtpmap:125 VP9/90000\r\na=rtcp-fb:125 goog-remb\r\na=rtcp-fb:125 transport-cc\r\na=rtcp-fb:125 ccm fir\r\na=rtcp-fb:125 nack\r\na=rtcp-fb:125 nack pli\r\na=fmtp:125 implementation_name=Internal;profile-id=0\r\na=rtpmap:119 rtx/90000\r\na=fmtp:119 apt=125\r\na=rtpmap:124 VP9/90000\r\na=rtcp-fb:124 goog-remb\r\na=rtcp-fb:124 transport-cc\r\na=rtcp-fb:124 ccm fir\r\na=rtcp-fb:124 nack\r\na=rtcp-fb:124 nack pli\r\na=fmtp:124 implementation_name=Internal;profile-id=2\r\na=rtpmap:118 rtx/90000\r\na=fmtp:118 apt=124\r\na=rtpmap:123 H264/90000\r\na=rtcp-fb:123 goog-remb\r\na=rtcp-fb:123 transport-cc\r\na=rtcp-fb:123 ccm fir\r\na=rtcp-fb:123 nack\r\na=rtcp-fb:123 nack pli\r\na=fmtp:123 implementation_name=VideoToolbox;level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=640c1f\r\na=rtpmap:117 rtx/90000\r\na=fmtp:117 apt=123\r\na=rtpmap:122 H264/90000\r\na=rtcp-fb:122 goog-remb\r\na=rtcp-fb:122 transport-cc\r\na=rtcp-fb:122 ccm fir\r\na=rtcp-fb:122 nack\r\na=rtcp-fb:122 nack pli\r\na=fmtp:122 implementation_name=VideoToolbox;level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f\r\na=rtpmap:116 rtx/90000\r\na=fmtp:116 apt=122\r\na=rtpmap:39 AV1/90000\r\na=rtcp-fb:39 goog-remb\r\na=rtcp-fb:39 transport-cc\r\na=rtcp-fb:39 ccm fir\r\na=rtcp-fb:39 nack\r\na=rtcp-fb:39 nack pli\r\na=fmtp:39 implementation_name=Internal\r\na=rtpmap:40 rtx/90000\r\na=fmtp:40 apt=39\r\na=rtpmap:115 red/90000\r\na=rtpmap:114 rtx/90000\r\na=fmtp:114 apt=115\r\na=rtpmap:121 ulpfec/90000\r\na=ssrc-group:FID 1404274606 2225194428\r\na=ssrc:1404274606 cname:ilZadlpJv8SVzJ1j\r\na=ssrc:1404274606 msid:c819fe8b-3bde-4b3f-98a3-4e30e38a7252 8f6b6c2a-3c2d-43d5-887b-e0f684389f8a\r\na=ssrc:2225194428 cname:ilZadlpJv8SVzJ1j\r\na=ssrc:2225194428 msid:c819fe8b-3bde-4b3f-98a3-4e30e38a7252 8f6b6c2a-3c2d-43d5-887b-e0f684389f8a\r\nm=application 54076 UDP/DTLS/SCTP webrtc-datachannel\r\nc=IN IP4 172.20.10.10\r\na=candidate:3094488124 1 udp 2122194687 172.20.10.10 54076 typ host generation 0 network-id 1 network-cost 50\r\na=candidate:880941575 1 udp 2122262783 2a02:b127:13:d0b6:c4dd:f172:74ee:1a5b 54672 typ host generation 0 network-id 2 network-cost 50\r\na=ice-ufrag:R/Hd\r\na=ice-pwd:SaezVaNICQAaVRNYV9qHyWv9\r\na=ice-options:trickle\r\na=fingerprint:sha-256 56:19:EB:54:5A:A3:50:8B:5C:AE:5B:84:6C:EB:D2:16:EA:A0:01:6C:F2:5D:F3:21:4B:1F:F9:3C:F4:E8:FD:C8\r\na=setup:actpass\r\na=mid:1\r\na=sctp-port:5000\r\na=max-message-size:262144\r\n'
        
        eFastapiMediaOutputProto = EApiMediaProto().ParseFromString(dataSerialize)
            

        endTime = time.time() - start_time
        
        print(eFastapiMediaOutputProto)
        
        IuLog.doDebug(__name__,f"test_DeserializationEvoProto time: {str(endTime)} avg: {endTime/self.COUNT_TEST}")
    '''
    
if __name__ == '__main__':
    unittest.main()
    
'''
class EnumBinaryType(enum.Enum):
    INT = 0
    LONG = 1
    FLOAT = 2
    DOUBLE = 3
    STRING = 4
    BOOL = 5
    BYTE = 6
    BYTES = 7

class IuBinaryN():
    
    @staticmethod
    def __toData(data: bytes) -> bytes:
        lenData = struct.pack('<I', len(data))
        return b'\x01' + lenData + data
    
    @staticmethod
    def toBytes(enumBinaryType: EnumBinaryType, value):
        if value is None:
            return b'\x00'
        
        if enumBinaryType == EnumBinaryType.INT:
            return IuBinaryN.__toData(struct.pack('<i', value))
        elif enumBinaryType == EnumBinaryType.LONG:
            return IuBinaryN.__toData(struct.pack('<q', value))
        elif enumBinaryType == EnumBinaryType.FLOAT:
            return IuBinaryN.__toData(struct.pack('<f', value))
        elif enumBinaryType == EnumBinaryType.DOUBLE:
            return IuBinaryN.__toData(struct.pack('<d', value))
        elif enumBinaryType == EnumBinaryType.STRING:
            return IuBinaryN.__toData(value.encode('utf-8'))
        elif enumBinaryType == EnumBinaryType.BOOL:
            return IuBinaryN.__toData(struct.pack('<?', value))
        elif enumBinaryType == EnumBinaryType.BYTE:
            return IuBinaryN.__toData(struct.pack('B', value))
        elif enumBinaryType == EnumBinaryType.BYTES:
            return IuBinaryN.__toData(value)
        else:
            raise ValueError(f"Unsupported type specified: {enumBinaryType}")

    @staticmethod
    def fromBytes(enumBinaryType: EnumBinaryType, dataValue: bytes):
        if dataValue[0] == 0:
            return None

        dataLen = struct.unpack('<I', dataValue[1:5])[0]
        data = dataValue[5:5 + dataLen]
        
        if enumBinaryType == EnumBinaryType.INT:
            return struct.unpack('<i', data)[0]
        elif enumBinaryType == EnumBinaryType.LONG:
            return struct.unpack('<q', data)[0]
        elif enumBinaryType == EnumBinaryType.FLOAT:
            return struct.unpack('<f', data)[0]
        elif enumBinaryType == EnumBinaryType.DOUBLE:
            return struct.unpack('<d', data)[0]
        elif enumBinaryType == EnumBinaryType.STRING:
            return data.decode('utf-8')
        elif enumBinaryType == EnumBinaryType.BOOL:
            return struct.unpack('<?', data)[0]
        elif enumBinaryType == EnumBinaryType.BYTE:
            return struct.unpack('B', data)[0]
        elif enumBinaryType == EnumBinaryType.BYTES:
            return data
        else:
            raise ValueError("Unsupported type specified")
    
    @staticmethod
    def toStream(enumBinaryType: EnumBinaryType, value, stream: io.BytesIO):
        stream.write(IuBinaryN.toBytes(enumBinaryType, value))
    
    @staticmethod
    def fromStream(enumBinaryType: EnumBinaryType, stream: io.BytesIO):
        flag = stream.read(1)
        if flag == b'\x00':
            return None
        
        len_bytes = stream.read(4)
        data_len = struct.unpack('<I', len_bytes)[0]
        data = stream.read(data_len)
        
        return IuBinaryN.fromBytes(enumBinaryType, b'\x01' + len_bytes + data)

class DataTest:
    
    
    
    def __init__(self):
        self.typeStr: str = None
        self.typeInt: int = None
        self.typeBool: bool = None
        self.typeBytes: bytes = None
        self.typeLong: int = None  # long
        self.typeFloat: float = None  # float
        self.typeDouble: float = None  # double
        
    
    def toBytes(self):
        stream = io.BytesIO()

        # Pack and write string
        encoded_str = self.typeStr.encode('utf-8') if self.typeStr is not None else None
        string_header = struct.pack('<BI', encoded_str is not None, len(encoded_str) if encoded_str else 0)
        stream.write(string_header)
        if encoded_str:
            stream.write(encoded_str)

        # Pack and write other types as a block to reduce function calls
        basic_types_format = '<i?Iqfd'
        basic_types_data = (
            self.typeInt, self.typeBool, len(self.typeBytes) if self.typeBytes is not None else 0,
            self.typeLong, self.typeFloat, self.typeDouble
        )
        stream.write(struct.pack(basic_types_format, *basic_types_data))

        # Write bytes if available
        if self.typeBytes:
            stream.write(self.typeBytes)

        return stream.getvalue()

    def fromBytes(self, data):
        stream = memoryview(data)
        offset = 0

        # Unpack header for string
        has_string, str_length = struct.unpack_from('<BI', stream, offset)
        offset += 5  # Size of B (1 byte) + I (4 bytes)
        if has_string:
            self.typeStr = stream[offset:offset + str_length].tobytes().decode('utf-8')
            offset += str_length
        else:
            self.typeStr = None
        
        # Unpack other types all at once
        format_to_unpack = '<i?Iqfd'
        self.typeInt, self.typeBool, bytes_length, self.typeLong, self.typeFloat, self.typeDouble = struct.unpack_from(format_to_unpack, stream, offset)
        offset += struct.calcsize(format_to_unpack)
        
        # Handle bytes
        if bytes_length > 0:
            self.typeBytes = stream[offset:offset + bytes_length].tobytes()
            offset += bytes_length
        else:
            self.typeBytes = None


    def toStream(self, stream: io.BytesIO):
        IuBinaryN.toStream(EnumBinaryType.STRING, self.typeStr, stream)
        IuBinaryN.toStream(EnumBinaryType.INT, self.typeInt, stream)
        IuBinaryN.toStream(EnumBinaryType.BOOL, self.typeBool, stream)
        IuBinaryN.toStream(EnumBinaryType.BYTES, self.typeBytes, stream)
        IuBinaryN.toStream(EnumBinaryType.LONG, self.typeLong, stream)
        IuBinaryN.toStream(EnumBinaryType.FLOAT, self.typeFloat, stream)
        IuBinaryN.toStream(EnumBinaryType.DOUBLE, self.typeDouble, stream)
        
    def fromStream(self, stream: io.BytesIO):
        self.typeStr = IuBinaryN.fromStream(EnumBinaryType.STRING, stream)
        self.typeInt = IuBinaryN.fromStream(EnumBinaryType.INT, stream)
        self.typeBool = IuBinaryN.fromStream(EnumBinaryType.BOOL, stream)
        self.typeBytes = IuBinaryN.fromStream(EnumBinaryType.BYTES, stream)
        self.typeLong = IuBinaryN.fromStream(EnumBinaryType.LONG, stream)
        self.typeFloat = IuBinaryN.fromStream(EnumBinaryType.FLOAT, stream)
        self.typeDouble = IuBinaryN.fromStream(EnumBinaryType.DOUBLE, stream)

    def to_bytes(self) -> bytes:
        stream = io.BytesIO()
        self.toStream(stream)
        return stream.getvalue()

    @staticmethod
    def from_bytes(data: bytes):
        stream = io.BytesIO(data)
        dataTest = DataTest()
        dataTest.fromStream(stream)
        return dataTest

def pack_data(record):
    stream = io.BytesIO()

    # Helper function to handle None checks and packing
    def pack_field(data, fmt):
        if data is None:
            stream.write(struct.pack('<B', 0))  # IsNone flag set to 0
        else:
            stream.write(struct.pack('<B', 1))  # IsNone flag set to 1
            if isinstance(data, (str, bytes)):
                # Handle strings and bytes differently due to variable length
                data_bytes = data.encode('utf-8') if isinstance(data, str) else data
                data_len = len(data_bytes)
                stream.write(struct.pack('<I', data_len))
                stream.write(data_bytes)
            else:
                # Fixed size types
                stream.write(struct.pack(fmt, data))

    # Packing all fields
    pack_field(record.typeStr, '<s')
    pack_field(record.typeInt, '<i')
    pack_field(record.typeBool, '<?')
    pack_field(record.typeBytes, '<s')
    pack_field(record.typeLong, '<q')
    pack_field(record.typeFloat, '<f')
    pack_field(record.typeDouble, '<d')

    return stream.getvalue()

def unpack_data(data):
    stream = io.BytesIO(data)
    result = {}

    # Helper function to unpack fields
    def unpack_field(fmt):
        is_none = struct.unpack('<B', stream.read(1))[0]
        if is_none == 0:
            return None
        if fmt == '<s':
            # Handle variable length data
            data_len = struct.unpack('<I', stream.read(4))[0]
            return stream.read(data_len)
        else:
            return struct.unpack(fmt, stream.read(struct.calcsize(fmt)))[0]

    # Unpacking all fields
    result['typeStr'] = unpack_field('<s')
    result['typeInt'] = unpack_field('<i')
    result['typeBool'] = unpack_field('<?')
    result['typeBytes'] = unpack_field('<s')
    result['typeLong'] = unpack_field('<q')
    result['typeFloat'] = unpack_field('<f')
    result['typeDouble'] = unpack_field('<d')

    return result



class DataTestProto:
    def __init__(self, typeStr=None, typeInt=None, typeBool=None, typeBytes=None, typeLong=None, typeFloat=None, typeDouble=None):
        self.typeStr = typeStr
        self.typeInt = typeInt
        self.typeBool = typeBool
        self.typeBytes = typeBytes
        self.typeLong = typeLong
        self.typeFloat = typeFloat
        self.typeDouble = typeDouble

    def serialize(self):
        """ Serialize the object to bytes with consideration for None values and efficient encoding."""
        stream = io.BytesIO()
        def write_varint(value):
            """ Encode an integer using varint encoding. """
            while value > 0x7f:
                stream.write(bytes((value & 0x7f | 0x80,)))
                value >>= 7
            stream.write(bytes((value,)))

        def write_bytes(data):
            """ Encode bytes, including strings, preceded by their length as a varint. """
            if data is None:
                stream.write(b'\x00')  # Presence flag for None
            else:
                stream.write(b'\x01')  # Presence flag for data present
                write_varint(len(data))
                stream.write(data)

        # Encode fields
        write_bytes(self.typeStr.encode('utf-8') if self.typeStr is not None else None)
        write_bytes(struct.pack('<i', self.typeInt) if self.typeInt is not None else None)
        write_bytes(bytes([self.typeBool]) if self.typeBool is not None else None)
        write_bytes(self.typeBytes)
        write_bytes(struct.pack('<q', self.typeLong) if self.typeLong is not None else None)
        write_bytes(struct.pack('<f', self.typeFloat) if self.typeFloat is not None else None)
        write_bytes(struct.pack('<d', self.typeDouble) if self.typeDouble is not None else None)

        return stream.getvalue()

    @staticmethod
    def deserialize(data):
        """ Deserialize data to reconstruct the DataTestProto object, handling optional values robustly. """
        stream = io.BytesIO(data)
        obj = DataTestProto()

        def read_varint():
            """ Decode a varint from the stream. """
            result, shift = 0, 0
            while True:
                byte = stream.read(1)[0]
                result |= ((byte & 0x7f) << shift)
                if not (byte & 0x80):
                    break
                shift += 7
            return result

        def read_bytes():
            """ Read bytes, checking for presence flag and reading length as varint if present. """
            if stream.read(1) == b'\x00':
                return None
            length = read_varint()
            return stream.read(length)

        # Decode fields, ensuring that each call to read_bytes is used correctly
        data = read_bytes()
        obj.typeStr = data.decode('utf-8') if data is not None else None
        
        data = read_bytes()
        obj.typeInt = struct.unpack('<i', data)[0] if data is not None else None
        
        data = read_bytes()
        obj.typeBool = bool(data[0]) if data is not None else None
        
        data = read_bytes()
        obj.typeBytes = data if data is not None else None
        
        data = read_bytes()
        obj.typeLong = struct.unpack('<q', data)[0] if data is not None else None
        
        data = read_bytes()
        obj.typeFloat = struct.unpack('<f', data)[0] if data is not None else None
        
        data = read_bytes()
        obj.typeDouble = struct.unpack('<d', data)[0] if data is not None else None

        return obj


'''