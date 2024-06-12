#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiAdmin

	EApiAdmin DESCRIPTION
	
"""
class EApiAdmin(EObject):

	VERSION:str="aad843e0d3665d9ce9e0cdbc6be3a484e6eff66a9daf66833292e1901d97c33d"

	def __init__(self):
		super().__init__()
		
		self.totp:bytes = None
		self.token:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteBytes(self.totp, stream)
		self._doWriteBytes(self.token, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.totp = self._doReadBytes(stream)
		self.token = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"totp length:{len(self.totp) if self.totp else 'None'}",
				f"token length:{len(self.token) if self.token else 'None'}",
							]) 
		return strReturn
	