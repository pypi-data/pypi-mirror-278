#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_api.entity.EApi import EApi
from evo_framework.core.evo_core_api.entity.EnumApiVisibility import EnumApiVisibility
from enum import Enum
#========================================================================================================================================

class EnumApiTunnel(Enum):
    LOCAL = 0
    CYBORGAI = 1
    NGROK = 2
    PINGGY = 3


"""EApiConfig

	this is EAction DESCRIPTION
	
"""
class EApiConfig(EObject):

	VERSION:str="522375abdb36150eb2abfdc838fe48145d8442932f2034b2cba34f38d20e014f"

	def __init__(self):
		super().__init__()
		self.enumApiVisibility:EnumApiVisibility = EnumApiVisibility.PRIVATE
		self.publicKey:bytes = None
		self.label:str = None
		self.description:str = None
		self.urlLogo:str = None
		self.remoteUrl:str = None
		self.remotePort:int = 443
		self.os:str = None
		self.mapEApi:EvoMap = EvoMap()
  
        #NOT SERIALIZE
		self.cyborgaiToken:str = None
		self.secretKey:bytes = None
		self.isFirstStart:bool = True
		self.localAddress:str = "0.0.0.0"
		self.localPort:int = 8001
		self.enumApiTunnel:EnumApiTunnel = EnumApiTunnel.LOCAL
  
	def toStream(self, stream):
		super().toStream(stream)	
		self._doWriteInt(self.enumApiVisibility.value, stream)
		self._doWriteBytes(self.publicKey, stream)
		self._doWriteStr(self.label, stream)
		self._doWriteStr(self.description, stream)
		self._doWriteStr(self.urlLogo, stream)
		self._doWriteStr(self.remoteUrl, stream)
		self._doWriteInt(self.remotePort, stream)
		self._doWriteStr(self.os, stream)
		self._doWriteMap(self.mapEApi, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		self.enumApiVisibility = EnumApiVisibility(self._doReadInt(stream))
		self.publicKey = self._doReadBytes(stream)
		self.label = self._doReadStr(stream)
		self.description = self._doReadStr(stream)
		self.urlLogo = self._doReadStr(stream)
		self.remoteUrl = self._doReadStr(stream)
		self.remotePort = self._doReadInt(stream)
		self.os = self._doReadStr(stream)
		self.mapEApi = self._doReadMap(EApi, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),					
				f"\tenumApiVisibility:{ self.enumApiVisibility  }",
				f"\tpublicKey:{ self.publicKey!r}",
				f"\tlabel:{self.label}",
				f"\tdescription:{self.description}",
				f"\turlLogo:{self.urlLogo}",
				f"\tremoteUrl:{self.remoteUrl}",
				f"\tremotePort:{self.remotePort}",
				f"\tos:{self.os}",
				f"\tmapEApi:{self.mapEApi}",					
    	]) 
		return strReturn