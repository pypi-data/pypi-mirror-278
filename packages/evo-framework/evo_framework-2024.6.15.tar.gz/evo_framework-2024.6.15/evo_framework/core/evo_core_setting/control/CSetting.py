import base64
import json
import os
import lz4.frame
from evo_framework.core.evo_core_setting.entity.ESetting import ESetting
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_system.utility.IuSystem import IuSystem
from urllib.parse import unquote
current_path = os.path.dirname(os.path.abspath(__file__))
class CSetting:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CSetting.__instance == None:
            cObject = CSetting()
            cObject.doInit()
        return CSetting.__instance

    def __init__(self):
        if CSetting.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            CSetting.__instance = self
            self.mapSetting = {}
             
    def doInit(self):
        try:
            self.eSettings = ESetting()
            try:
               self.eSettings.path_output =  IuSystem.do_sanitize_path( f"{current_path}/../../../../assets/")
            except Exception as exception:
                IuLog.doException(__name__,exception)
            
        
            # Read the base64-encoded JSON from the environment variable
            encoded_json =os.environ.get('SETTINGS_JSON')
            
            if(encoded_json ==None):
                raise Exception("ERROR_SETTINGS_JSON_environment use the utility register_cyborgai_env.sh")
            
            
            #print(encoded_json)

            # Decode base64-encoded data
            decoded_data = base64.b64decode(encoded_json)

                # Decompress the decoded data
            decompressed_data = lz4.frame.decompress(decoded_data)

                # URL-decode the decompressed data
            json_str = unquote(decompressed_data.decode())

            # Load the JSON string as a Python object
            self.mapSetting = json.loads(json_str)
            
            self.isLocal= self.mapSetting["IS_LOCAL"]
        
            if self.isLocal:
                self.URL_LOCAL = self.mapSetting["BASE_LOCAL_URL"]
            
                self.ENVORIMENT="dev"
            else:
                self.URL_LOCAL = "BASE_REMOTE_URL"
                self.ENVORIMENT="prod"
            '''
            if (self.isLocal):
                print(self.mapSetting)
                print(self.URL_LOCAL)
            '''
        except Exception as exception:
            IuLog.doError(__name__,f"{exception}")
            #IuLog.doException(__name__,exception)
            #raise exception
    
    def doGet(self, key:str):
        try:
            return self.mapSetting.get(key)
        except Exception as exception:
            IuLog.doError(__name__,f"{exception}")
            return None
            
            
        
        
