from datetime import datetime, timezone
import uuid
import time
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash

class IuKey:
    countNonce = 0
    @staticmethod
    def generateId(input_string:str=None):
        IuKey.countNonce +=1 
        if input_string == None:
            current_time_ns = time.time_ns()
            input_string = str(current_time_ns)
            
        iD = IuCryptHash.toSha256(f"{input_string}{IuKey.countNonce}")
    
        return iD
    
    @staticmethod
    def generateTime():
        now = datetime.now(timezone.utc)  # Get the current time in UTC
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # The Unix epoch time in UTC
        time_delta = now - epoch
        timeUtc = int(time_delta.total_seconds() * 1000)  # Convert to milliseconds
        return timeUtc
       
        
        
        
        