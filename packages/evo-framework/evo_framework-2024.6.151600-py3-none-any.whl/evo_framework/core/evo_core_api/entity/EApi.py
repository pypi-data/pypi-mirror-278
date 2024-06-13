#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApi

	this is EAPI DESCRIPTION
	
"""
class EApi(EObject):

	VERSION:str="da9425fde78f3f2dbb9c52ba7a93787960d94e81751ae8594a64f678a80060d3"

	def __init__(self):
		super().__init__()
		self.description:str = None
		self.isStream:bool = None
		self.input:str = None
		self.output:str = None
  
		#NOT_SERIALIZED
		self.context = {}
		self.callback = None
		self.isEnabled:bool = True
  
	def toStream(self, stream):
		super().toStream(stream)
		self._doWriteStr(self.description, stream)
		self._doWriteBool(self.isStream, stream)
		self._doWriteStr(self.input, stream)
		self._doWriteStr(self.output, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		self.description = self._doReadStr(stream)
		self.isStream = self._doReadBool(stream)
		self.input = self._doReadStr(stream)
		self.output = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),				
				f"\tdescription:{ self.description  }",
				f"\tisStream:{ self.isStream  }",
				f"\tinput:{ self.input  }",
				f"\toutput:{ self.output  }",
							]) 
		return strReturn
	