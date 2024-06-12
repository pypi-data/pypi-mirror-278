#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto
#========================================================================================================================================
"""ERequest

	ERequest DESCRIPTION
	
"""
class ERequest(EObject):

	VERSION:str="2aafac6a76b23b255eed9371f540c0d5b0f1fc5bf47cbd6c4fcba659dee2f7b6"

	def __init__(self):
		super().__init__()
		self.enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC
		self.pk:bytes = None
		self.cipher:bytes = None
		self.sign:bytes = None
		self.hash:bytes = None
		self.chunk:int = None
		self.chunkTotal:int = None
		self.data:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		self._doWriteInt(self.enumApiCrypto.value, stream)
		self._doWriteBytes(self.pk, stream)
		self._doWriteBytes(self.cipher, stream)
		self._doWriteBytes(self.sign, stream)
		self._doWriteBytes(self.hash, stream)
		self._doWriteInt(self.chunk, stream)
		self._doWriteInt(self.chunkTotal, stream)
		self._doWriteBytes(self.data, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)	
		self.enumApiCrypto = EnumApiCrypto(self._doReadInt(stream))
		self.pk = self._doReadBytes(stream)
		self.cipher = self._doReadBytes(stream)
		self.sign = self._doReadBytes(stream)
		self.hash = self._doReadBytes(stream)
		self.chunk = self._doReadInt(stream)
		self.chunkTotal = self._doReadInt(stream)
		self.data = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),					
				f"\tenumApiCrypto:{self.enumApiCrypto}",
				f"pk length:{len(self.pk) if self.pk else 'None'}",
				f"cipher length:{len(self.cipher) if self.cipher else 'None'}",
				f"sign length:{len(self.sign) if self.sign else 'None'}",
				f"hash length:{len(self.hash) if self.hash else 'None'}",
				f"\tchunk:{self.chunk}",
				f"\tchunkTotal:{self.chunkTotal}",
				f"data length:{len(self.data) if self.data else 'None'}",
							]) 
		return strReturn
	