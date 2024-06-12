logo:str="""
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
"""
from evo_framework.core import *
from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_api.entity.EApiConfig import EApiConfig
from evo_framework.core.evo_core_key.utility.IuKey import IuKey
from evo_framework.core.evo_core_crypto.utility.IuCryptEC import IuCryptEC
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_system.utility.IuSystem import IuSystem
from evo_framework.core.evo_core_convert.utility.IuConvert import IuConvert
from evo_framework.core.evo_core_setting.control.CSetting import CSetting
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_api.entity.EActionTask import EActionTask
from evo_framework.core.evo_core_api.entity.ERequest import ERequest
from evo_framework.core.evo_core_api.entity.EResponse import EResponse
from evo_framework.core.evo_core_api.entity.EApi import EApi
from evo_framework.core.evo_core_api.entity.EAction import EAction
from evo_framework.core.evo_core_api.entity.EnumApiAction import EnumApiAction
from evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto
from evo_framework.core.evo_core_api.entity.EnumApiType import EnumApiType
from evo_framework.core.evo_core_api.utility.IuApi import IuApi
import lz4.frame
import requests
from functools import partial
# ---------------------------------------------------------------------------------------------------------------------------------------
# CApi
# ---------------------------------------------------------------------------------------------------------------------------------------
class CApiFlow():
    __instance = None

    def __init__(self):
        if CApiFlow.__instance is not None:
            raise Exception("ERROR_SINGLETON")
        else:
            super().__init__()
            CApiFlow.__instance = self
            self.version = "20240411"
            self.path = os.path.dirname(os.path.abspath(__file__))
            self.__url_server = "https://cyborgai-api.fly.dev"
            #self.__url_server= 'http://127.0.0.1:8000'
            self.__pk_server = "06042123ca30c6ca45e700a1e3675c23825a9d0b52309e17b96f90ba86c1a1ca002ca04e133069ff93a43fc885d24d9283d0c699af29104aacb88c6a371e1cca" #pinning           
           
            self.__url_cyborgai = f"{ self.__url_server}/v2/set_node/"    
            self.eApiConfig:EApiConfig = EApiConfig()
            self.mapFileHandler = {}
            self.mapEFileConfig = EvoMap()
            self.isSetEConfig:bool = False 
            self.mapEAction:EvoMap = EvoMap()
            self.mapERequest:EvoMap = EvoMap()
            self.isEndPoint = False
            
# ---------------------------------------------------------------------------------------------------------------------------------------         
    @staticmethod
    def getInstance():
        if CApiFlow.__instance is None:
            cObject=CApiFlow()
        return CApiFlow.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    def doInit(self, isEndPoint=False):
        try:      
            self.isEndPoint = isEndPoint
            CSetting.getInstance().doInit()
            #@TODO:move to PQ 
            self.eApiConfig.enumApiCrypto = EnumApiCrypto.ECC
            self.eApiConfig.os = IuSystem.get_os_info()        
            print(logo)  
            self.__doGenenerateCryptoKey()
                       
            if (not self.isEndPoint):
                
                eApi = EApi()
                eApi.id = "evo-get_eapiconfig"
                eApi.doGenerateTime()
                eApi.isStream = False
                eApi.callback = self.doGetEApiConfig
                     
                eApi.output = f"{EApiConfig.__module__}|{EApiConfig.VERSION}"
                eApi.description = "get EApiConfig"
                
                self.doSetEApi(eApi)
            else:
                IuLog.doVerbose(__name__, f"\nPUBLICK KEY:\n{IuConvert.toHex(self.eApiConfig.publicKey)}")
                
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception
# ---------------------------------------------------------------------------------------------------------------------------------------    
    async def doInitEApiConfig(self):
        try: 
    
            IuLog.doVerbose(__name__, f"eApiConfig:\n{self.eApiConfig}\n")
            
            if (not self.isEndPoint):
                eResponseCyborgAI = await self.__doSetEApiConfig()
                self.eApiConfig.cyborgaiToken = eResponseCyborgAI.data.decode("utf-8")
                IuLog.doVerbose(__name__, f"cyborgai_token:{  self.eApiConfig.cyborgaiToken}")
            
           
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __doGenenerateCryptoKey(self ):
        try:
  
            if self.eApiConfig.enumApiCrypto == EnumApiCrypto.ECC:
                privateKeyStr=None
                try:
                    #print( CSetting.getInstance().mapSetting)
                    privateKeyStr = CSetting.getInstance().mapSetting["CYBORGAI_SK"]  
                except Exception as exception:
                    IuLog.doDebug(__name__,"EMPTY_SK")
    
                if privateKeyStr is None:
                    sk, pk = IuCryptEC.generate_key_pair()
                    IuLog.doVerbose(__name__, f"key generate :{sk} {pk}")
                    self.eApiConfig.secretKey = sk
                    self.eApiConfig.publicKey = pk.to_string()
                    self.eApiConfig.isFirstStart = True 
                    IuLog.doVerbose(__name__, f"\nSECRET KEY:\n{IuConvert.toBase64(sk.to_string())}\nATTENTION NOT SHARE")
          
                else:
                    sk, pk = IuCryptEC.get_key_pair(privateKeyStr)
                    IuLog.doVerbose(__name__, f"key regenerate :{sk} {pk}")
                    self.eApiConfig.secretKey = sk
                    self.eApiConfig.publicKey = pk.to_string()   
                    self.eApiConfig.isFirstStart = False
                   
            else:
                #TODO:add PQ crypto
                raise Exception(f"NOT_VALID_{self.eApiConfig.enumApiCrypto}")
            
            IuLog.doVerbose(__name__, f"sk,{self.eApiConfig.secretKey}")
            self.eApiConfig.id = IuCryptHash.toSha256(self.eApiConfig.publicKey)
            self.eApiConfig.doGenerateTime()
            
            if self.eApiConfig.secretKey is None:
                raise Exception("NOT_VALID_PRIVATE_KEY")
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doSetEApiConfig(self) -> EResponse:
        try:
            IuLog.doVerbose(__name__, f"self{self.eApiConfig}")
            
            eRequest = ERequest()    
            eRequest.id = self.eApiConfig.id
            eRequest.time = IuKey.generateTime()
            eRequest.data =self.eApiConfig.toBytes()
            eRequest.hash = IuCryptHash.toSha256Bytes(eRequest.data)
          
            sign = IuCryptEC.sign_data( eRequest.hash, self.eApiConfig.secretKey)
            eRequest.pk = self.eApiConfig.publicKey
            eRequest.sign = sign
            
   
            data =  lz4.frame.compress(eRequest.toBytes()) #IuApi.ToERequestLZ4(eRequest)
  
            headers = {
                "Content-Type": "application/binary",
                # 'Authorization': 'Bearer YourAuthToken',
            }
            IuLog.doDebug(__name__, f"self.__url_cyborgai:{self.__url_cyborgai}")

            response = requests.post(
                self.__url_cyborgai, data=data, headers=headers
            )
            IuLog.doDebug(__name__, f"response.status_code:{response.status_code}")

            if response.status_code == 200:
                dataEResponse = response.content
                data =  lz4.frame.decompress(dataEResponse) 
                eResponse = EResponse()
                eResponse.fromBytes(data)
                
                hash = IuCryptHash.toSha256Bytes(eResponse.data)
                
                IuLog.doVerbose(__name__,f"CHUNK HASH: {eResponse.id} {hash!r} hash:{ eResponse.hash!r} { eResponse.hash==hash}")
                if hash !=  eResponse.hash:
                    raise Exception(f"NOT_VALID_HASH_{ eResponse.hash.hex()}")
                
                IuLog.doVerbose(__name__,f"checkSign: {eResponse}")
                
                pkServer = IuConvert.fromHex(self.__pk_server)
                isValid = IuCryptEC.verify_data(eResponse.hash, eResponse.sign, pkServer)
                IuLog.doVerbose(__name__,f"checkSign: {eResponse.id} {eResponse.hash!r} isValid:{isValid}")
                if not isValid:
                        raise Exception("NOT_VALID_SIGN")
                
                self.eApiConfig.cyborgaiToken = eResponse.data.decode()  
                
                self.isSetEConfig = True
                
            else:
                raise Exception(f"ERROR_FAILED_REGISTER_PEER_TO_CYBORGAI:{response.status_code}")

            return eResponse
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------    
    async def onRequest(self, dataERequest:bytes, checkSign:bool=False):
        try:

            dataDecompressed = lz4.frame.decompress(dataERequest)
            eRequest = IuApi.toEObject(ERequest(),dataDecompressed)
            
            if isinstance(eRequest, ERequest):
                if (len(eRequest.id) < 64):
                    raise Exception(f"NOT_VALID_ID_{eRequest.id}")
                
                hash = IuCryptHash.toSha256Bytes(eRequest.data)
                
                IuLog.doVerbose(__name__,f"CHUNK HASH: {eRequest.chunk} {hash!r} hash:{ eRequest.hash!r} { eRequest.hash==hash}")
                if hash !=  eRequest.hash:
                    raise Exception(f"NOT_VALID_HASH_{ eRequest.hash.hex()}")
                
                if checkSign:
                    if not eRequest.pk:
                        raise Exception("NOT_VALID_PK")
                    IuLog.doVerbose(__name__,f"checkSign: {eRequest}")
                    #signSha256 = IuCryptHash.toSha256Bytes(eRequest.id.encode() + hash)
                    signSha256 = IuCryptHash.toSha256Bytes( hash)
                    isValid = IuCryptEC.verify_data(eRequest.hash, eRequest.sign, eRequest.pk)
                    IuLog.doVerbose(__name__,f"checkSign: {eRequest.id} {signSha256!r} isValid:{isValid}")
                    if not isValid:
                         raise Exception("NOT_VALID_SIGN")
                  
                
                file_path = f"/tmp/{eRequest.id}.eam"
                bytesChunk = eRequest.data
                
                IuLog.doVerbose(__name__,f"eRequest:{eRequest}")
            
                if eRequest.chunk == eRequest.chunkTotal:                
                    dataReturn = None             
                    if eRequest.id in self.mapFileHandler:
                        file = self.mapFileHandler[eRequest.id]   
                        await file.write(bytesChunk)
                        await file.flush()    
                        file.close()
                        del self.mapFileHandler[eRequest.id]
                        # channel.send(dataResponse)
                                        
                        async with aiofiles.open(file_path, mode='rb') as file:
                            dataReturn = await file.read()          
                        IuLog.doDebug(__name__,f"COMPLETE CHUNK:{len(dataReturn)}")
                      
                    else:
                        dataReturn = bytesChunk    
                        
                    eRequest.doGenerateTime()
                    self.mapERequest.doSet(eRequest)
                    return (eRequest.id ,dataReturn)  
              
                else:   
                    if eRequest.id not in self.mapFileHandler:
                        file = await aiofiles.open(file_path, mode='ab')
                        self.mapFileHandler[eRequest.id ] = file
                    
                    file = self.mapFileHandler[eRequest.id]   
                    await file.write(bytesChunk)
                    await file.flush()
                
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception
# ---------------------------------------------------------------------------------------------------------------------------------------    
    async def onResponse(self, iDERequest:str, data:bytes, chunk:int =1, chunkTotal:int = 1) ->bytes:
        try:
               
            IuLog.doDebug(__name__, f"self.eApiConfig.:{self.eApiConfig}")
            
            hashData = IuCryptHash.toSha256Bytes(data)
            sign = IuCryptEC.sign_data(hashData, self.eApiConfig.secretKey)
            eResponse = EResponse()
            eResponse.id = iDERequest
            eResponse.doGenerateTime()
            eResponse.data = data
            eResponse.chunk = chunk
            eResponse.chunkTotal = chunkTotal
            eResponse.hash = hashData
            eResponse.sign = sign
            #eResponse.pk = self.eApiConfig.publicKey
            eResponse.data = data 
            IuLog.doVerbose(__name__,f"eResponse:{eResponse}")
            dataOut=eResponse.toBytes()
                  
            dataEResponse = lz4.frame.compress(dataOut)
            
            eRequest:ERequest = self.mapERequest.doGet(iDERequest)    
           
            if eRequest:
                time = IuKey.generateTime()
                IuLog.doDebug(__name__,
                                f"response:{eRequest.id} time:{str(time - eRequest.time)}s ",
                            )
                self.mapERequest.doDel(iDERequest) 
            
            return dataEResponse
           
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

# ---------------------------------------------------------------------------------------------------------------------------------------
    def doSetEApi(self,eApi:EApi):
        try:
            
            self.eApiConfig.mapEApi.doSet(eApi) 
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------  
    def doGetEApi(self,action) ->EApi:
        try:
            eApi = self.eApiConfig.mapEApi.doGet(action)

            if isinstance(eApi, EApi):
               return eApi
               
            else:
                raise Exception(f"NOT_VALID_{action}")
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------  
    def doPrintMapEApi(self):
        try:
            listStr =""
            count = 1
            for key in self.eApiConfig.mapEApi.keys():
                eApi:EApi = self.eApiConfig.mapEApi.doGet(key)
                callback = eApi.callback
                idApi =str(eApi.id).ljust(25," ")
                countStr= str(count).ljust(4," ")
                listStr= "\n".join([listStr, f"{countStr} {idApi} => {callback.__module__}.{callback.__name__}"])
                count+=1

            IuLog.doInfo("api", f"{listStr}\n")
          
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------  
    async def onAction(self, eApi:EApi, eActionTask:EActionTask):
        try:
            eActionTask.eActionOutput = await eApi.callback( eActionTask.eActionInput)
            return eActionTask.eActionOutput
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------     
    async def onActionStream(self, eApi:EApi, eActionTask:EActionTask) :
        try:
            async for eActionOutput in eApi.callback( eActionTask.eActionInput):
                yield eActionOutput
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception       
# ---------------------------------------------------------------------------------------------------------------------------------------  
    async def onActionCallBack(self, eApi:EApi, eActionTask:EActionTask):
        try:
            eActionTask.eActionOutput = await eApi.callback( eActionTask.eActionInput)
            await eActionTask.evoCallback(eActionTask)             
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------     
    async def onActionStreamCallback(self, eApi:EApi, eActionTask:EActionTask) :
        try:
            async for eActionOutput in eApi.callback( eActionTask.eActionInput):
                eActionTask.eActionOutput = eActionOutput
                await eActionTask.evoCallback(eActionTask)  
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# --------------------------------------------------------------------------------------------------------------------------------------- 
    async def doActionCallBack(self, eActionTask:EActionTask):
        try:
            IuLog.doDebug(__name__,f"OnActionThread: {eActionTask}")
            eApi = self.doGetEApi(eActionTask.action)

            eActionTask.isStreamAction = eApi.isStream
            if (eApi.isStream):  
                self.run_in_background(self.onActionStreamCallback, eApi, eActionTask)
            else:  
                self.run_in_background(self.onActionCallBack, eApi, eActionTask)  
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------          
    def start_async_loop(self, loop):
        try:
            asyncio.set_event_loop(loop)
            loop.run_forever()
        except Exception as exception:
            IuLog.doException(__name__, exception)
# ---------------------------------------------------------------------------------------------------------------------------------------
    def run_in_background(self, target, actionFunc, eActionTask:EActionTask):
        try:
            eActionTask.loop = asyncio.new_event_loop()
            eActionTask.threadBackground = threading.Thread(target=self.start_async_loop, args=(eActionTask.loop,), daemon=True)
            eActionTask.threadBackground.start()
            self.mapEAction.doSet(eActionTask)
            
            if asyncio.iscoroutinefunction(target):
                coroutine = partial(target, actionFunc, eActionTask)
                asyncio.run_coroutine_threadsafe(coroutine(), eActionTask.loop)
            else:
                raise TypeError(f"target function {target.__name__} must be an asynchronous function")
        except Exception as exception:
            IuLog.doException(__name__, exception)
 
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doStop(self):
        try:
            for eAction in self.mapEAction.__dictionary.values:
                try:
                    if isinstance(eAction, EActionTask):
                        if eAction.loop:
                            asyncio.run_coroutine_threadsafe(eAction.loop.stop(), eAction.loop)
                            eAction.threadBackground.join() 
                            eAction.loop = None
                            eAction.threadBackground = None
                except Exception as exception:
                    IuLog.doException(__name__, exception)
        except Exception as exception:
            IuLog.doException(__name__, exception)
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetEApiConfig(self, eAction: EAction) -> EAction:
        try:
            IuLog.doDebug(__name__,f"doGetEApiConfig: {eAction}")
            eAction.input = None
            
            eAction.output = self.eApiConfig.toBytes()
            
            IuLog.doDebug(__name__,f"eAction output: {eAction}")
            return eAction     
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------