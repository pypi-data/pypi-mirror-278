#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiText

	EApiFile DESCRIPTION
	
"""
class EApiText(EObject):

	VERSION:str="b9dad9a4e65a9619c0c509f335cde9cbfb43ff3fa48d77d1761a6d071239cc5b"

	def __init__(self):
		super().__init__()
		self.header:str = None
		self.language:str = "NONE"
		self.text:str = None
		self.isComplete:bool = None
		self.isError:bool = None
		self.error:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		self._doWriteStr(self.header, stream)
		self._doWriteStr(self.language, stream)
		self._doWriteStr(self.text, stream)
		self._doWriteBool(self.isComplete, stream)
		self._doWriteBool(self.isError, stream)
		self._doWriteStr(self.error, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		self.header = self._doReadStr(stream)
		self.language = self._doReadStr(stream)
		self.text = self._doReadStr(stream)
		self.isComplete = self._doReadBool(stream)
		self.isError = self._doReadBool(stream)
		self.error = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),				
				f"\theader:{self.header}",
				f"\tlanguage:{self.language}",
				f"\ttext:{self.text}",
				f"\tisComplete:{self.isComplete}",
				f"\tisError:{self.isError}",
				f"\terror:{self.error}",
							]) 
		return strReturn
	