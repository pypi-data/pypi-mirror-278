
#========================================================================================================================================
#                                                                                                                                       #
#                                 00000                                                                                                 #
#                                00   00                                                                                                #
#                 0000          0     0                                                                                                 #
#                800  007        0     0                                     0000                                                       #
#                0      7       00 00000                  4800000008         0  0                                      800008   6882    #
#                0     000  006 0 00                    580        08        0  0                                     80    0      8    #
#                800000  0000 00000                    28   00000   0000  0000  000000000000000000000000000000000    80  9  09  9  8    #
#                     000   0    00     8006           8   04   8000   0000  0        00        00              0    0   0   09 9  8    #
#                      0  0       0000000  083         8   8     8800   00  00  0000      0000   0   00  0000   0   00  000   0 9  8    #
#            58000800000          00    0    3         28  0088800 000  0   00  00 00     00 00  0  00   0000   0  00         089  8    #
#            8    00   00         00000     83          8     0     800    000   000   0   000   0  000         0  0   00000   08  8    #
#                  0000000      000   8000084           3880      008 00  00 0  0    0000      000  0 000   0   0  0  08   90   9  8    #
#            8     0     00000000                          68000008  00  00  000000000  00000000 0000 0  0000  00  0000     68088882    #
#            4800008         0  00                                   0   0                            00      00                        #
#                           000  000                                 00000                             00000000                         #
#                           0 0    0                                                                                                    #
#                           0      0                                                                                                    #
#                           00000000                                                                                                    #
#                                                                                                                                       #
# CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International       https://github.com/cyborg-ai-git     #
#========================================================================================================================================

from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_binary.utility.IuBinary import IuBinary
from evo_framework.core.evo_core_key.utility.IuKey import IuKey
import io
import struct

#cached
int_packer = struct.Struct('<l')
long_packer = struct.Struct('<q')
float_packer = struct.Struct('<f')
double_packer = struct.Struct('<d')
bool_packer = struct.Struct('<?')

class EObject(object):
    #annotatioon;

    def __init__(self):
        self.id:str = ""
        self.time:int = IuKey.generateTime()
           
       # self.version:bytes = b""
        #self.module:str = self.__class__.__module__
        #self.format="<l{len_id}{id}<l{time}"
        
    def doGenerateID(self):
        self.id = IuKey.generateId()
        
    def doGenerateTime(self):
        self.time = IuKey.generateTime()
        
    def toBytes(self) -> bytes:  
        with io.BytesIO() as stream:
            self.toStream(stream)
            return stream.getvalue()
        
    def fromBytes(self, data: bytes):
        if data:
            with io.BytesIO(data) as stream:
                self.fromStream(stream)
            return self
        return None
    
    def toStream(self, stream): 
        self._doWriteStr(self.id,stream)
        self._doWriteLong(self.time,stream)
        #self._doWriteBytes(self.version,stream)
         
    def fromStream(self, stream):
        self.id=self._doReadStr(stream)
        self.time = self._doReadLong(stream)
       # self.versio = self._doReadBytes(stream)
        
    def _doWriteStr(self, value: str, stream: io.BytesIO):
        if value is None:
            stream.write(int_packer.pack(-1))
        else:
            encoded = value.encode('UTF-8')
            stream.write(int_packer.pack(len(encoded)) + encoded)

    def _doReadStr(self, stream: io.BytesIO) -> str:
        length = int_packer.unpack(stream.read(4))[0]
        if length == -1:
            return None
        return stream.read(length).decode('UTF-8')
    
    def _doWriteLanguage(self, value: str, stream: io.BytesIO):
        if value is None:
            stream.write(int_packer.pack(-1))
        else:
            encoded = value.encode('UTF-8')
            stream.write(int_packer.pack(len(encoded)) + encoded)

    def _doReadLanguage(self, stream: io.BytesIO) -> str:
        length = int_packer.unpack(stream.read(4))[0]
        if length == -1:
            return None
        return stream.read(length).decode('UTF-8')

    def _doWriteInt(self, value: int, stream: io.BytesIO):
       
        stream.write(int_packer.pack(value if value is not None else -1))

    def _doReadInt(self, stream: io.BytesIO) -> int:
        return int_packer.unpack(stream.read(4))[0]

    def _doWriteLong(self, value: int, stream: io.BytesIO):
        stream.write(long_packer.pack(value if value is not None else -1))

    def _doReadLong(self, stream: io.BytesIO) -> int:
        return long_packer.unpack(stream.read(8))[0]

    def _doWriteBytes(self, value: bytes, stream: io.BytesIO):
        if value is None:
            self._doWriteInt(-1,stream)
        else:
            self._doWriteInt(len(value),stream)
            stream.write(value)
   
    def _doReadBytes(self, stream: io.BytesIO) -> bytes:
        length = self._doReadInt(stream)
        if length == -1:
            return None
        return stream.read(length)

    def _doWriteFloat(self, value: float, stream: io.BytesIO):
        stream.write(float_packer.pack(value if value is not None else -1.0))

    def _doReadFloat(self, stream: io.BytesIO) -> float:
        return float_packer.unpack(stream.read(4))[0]

    def _doWriteDouble(self, value: float, stream: io.BytesIO):
        stream.write(double_packer.pack(value if value is not None else -1.0))

    def _doReadDouble(self, stream: io.BytesIO) -> float:
        return double_packer.unpack(stream.read(8))[0]

    def _doWriteBool(self, value: bool, stream: io.BytesIO):
        stream.write(bool_packer.pack(value if value is not None else False))

    def _doReadBool(self, stream: io.BytesIO) -> bool:
        return bool_packer.unpack(stream.read(1))[0]
     
    def _doWriteEObject(self, value, stream: io.BytesIO):
        if value is None:
            self._doWriteBool(True,stream)
        else:
            self._doWriteBool(False,stream)
            value.toStream(stream) 

    def _doReadEObject(self, EClass, stream: io.BytesIO):
        isNull = self._doReadBool(stream) 
        if isNull:
            return None
        eObject = EClass()  
        eObject.fromStream(stream)
        return eObject
    
    def _doWriteMap(self, value:EvoMap, stream: io.BytesIO):
        if value is None:
            self._doWriteInt(-1,stream)
        else:
            self._doWriteInt(len(value.keys()),stream)
           
            for obj in value.values():
                self._doWriteEObject(obj, stream)  
    
    def _doReadMap(self, EClass, stream: io.BytesIO) -> EvoMap:
        count = self._doReadInt(stream)  # Directly read and unpack count
        if count == -1:
            return None
        value = EvoMap()
        for _ in range(count):
            eObject = self._doReadEObject(EClass, stream)
            value.doSet(eObject)  
        return value

    def __str__(self):
        return  "\n".join([ 
                            f"\n{self.__class__.__name__}:",
                            f"\tid: {self.id}",
                            f"\ttime: {self.time}",
                          ]
                        )
      
    def toString(self) -> str:
        return  self.__str__()
        
    def to_dict_with_types(self):
        attr_dict = {}
        annotations = self.__class__.__annotations__ 

        for attr in annotations.keys():
            value = getattr(self, attr, None)
            attr_type = type(value).__name__ if value is not None else annotations[attr].__name__
            attr_dict[attr] = {'value': value, 'type': attr_type}

        # Include any additional instance attributes not present in annotations
        for attr in set(vars(self).keys()) - set(annotations.keys()):
            value = getattr(self, attr, None)
            attr_dict[attr] = {
                'value': value,
                'type': type(value).__name__
            }

        return attr_dict
