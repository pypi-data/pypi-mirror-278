# =======================================================================================================================================
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
# =======================================================================================================================================

from evo_framework.core import *
from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_key.utility.IuKey import IuKey
from evo_framework.core.evo_core_api.control.CApiFlow import CApiFlow
from evo_framework.core.evo_core_api.entity.EApi import EApi
from evo_framework.core.evo_core_api.entity.EnumApiType import EnumApiType

# ------------------------------------------------------------------------------------------------
# CActionApi
# ------------------------------------------------------------------------------------------------
class CApi():

# ------------------------------------------------------------------------------------------------
    def __init__(self):
            super().__init__()
            self.mapEApi = EvoMap()
            self.mapEApiMap = EvoMap()
            self.current_path = os.path.dirname(os.path.abspath(__file__))
            
            
# ------------------------------------------------------------------------------------------------          
    @abstractmethod
    def doAddApi(self):
        pass
# ------------------------------------------------------------------------------------------------
    async def doAction(self, eAction):
        try:
            IuLog.doVerbose(__name__, f"doAction: {eAction}")
            
            await CApiFlow.getInstance().doActionCallBack(eAction)
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ------------------------------------------------------------------------------------------------
    
    def newApi(self, id:str, callback, input:Type, output:Type, isStream:bool=False,isEnabled=True, description:str="", urlEntity:str=""  ) -> EApi:
        try: 
            eApi = EApi()
            eApi.id = id
            eApi.doGenerateTime()
            eApi.callback = callback
            eApi.isStream = isStream
            eApi.description = description
            eApi.isEnabled = isEnabled
            
            if hasattr(input, "VERSION"):
                 eApi.input = f"{input.__module__}|{input.VERSION}"
            else:
                raise Exception(f"ERROR_NOT_VALID_INPUT_ECLASS_{input.__module__}")
            
            if hasattr(output, "VERSION"):
                 eApi.output = f"{output.__module__}|{output.VERSION}"
            else:
                raise Exception(f"ERROR_NOT_VALID_OUTPUT_ECLASS_{output.__module__}")
            
            if eApi.isEnabled:
                self.mapEApi.doSet(eApi)
                CApiFlow.getInstance().doSetEApi(eApi)
            
            return eApi     
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception

