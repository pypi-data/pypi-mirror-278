#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiFile

	EApiFile DESCRIPTION
	
"""
class EApiFile(EObject):

	VERSION:str="0730dc08c00ef118a08b1a9a783a957624b265c97ee9ea7b0b9082c2913fe538"

	def __init__(self):
		super().__init__()
		
		self.isUrl:bool = None
		self.name:str = None
		self.ext:str = None
		self.hash:bytes = None
		self.data:bytes = None
		self.url:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteBool(self.isUrl, stream)
		self._doWriteStr(self.name, stream)
		self._doWriteStr(self.ext, stream)
		self._doWriteBytes(self.hash, stream)
		self._doWriteBytes(self.data, stream)
		self._doWriteStr(self.url, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.isUrl = self._doReadBool(stream)
		self.name = self._doReadStr(stream)
		self.ext = self._doReadStr(stream)
		self.hash = self._doReadBytes(stream)
		self.data = self._doReadBytes(stream)
		self.url = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tisUrl:{self.isUrl}",
				f"\tname:{self.name}",
				f"\text:{self.ext}",
				f"	hash length:{len(self.hash) if self.hash else 'None'}",
				f"	data length:{len(self.data) if self.data else 'None'}",
				f"\turl:{self.url}",
							]) 
		return strReturn
	