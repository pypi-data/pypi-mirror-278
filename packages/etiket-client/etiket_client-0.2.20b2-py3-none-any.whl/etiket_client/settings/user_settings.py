import dataclasses, datetime

from typing import ClassVar

from etiket_client.settings.folders import get_user_data_dir
from etiket_client.settings.saver import settings_saver

@dataclasses.dataclass
class user_settings(settings_saver):
    user_name : str = None
    access_token : str = None
    access_token_expiration : int = None
    refresh_token : str = None
    
    system_is_measurement_PC : bool = None
    measurement_PC : str = None
    API_token  : str = None
    
    verbose : bool = True
    last_version_check : int = None
	
    current_scope : str = None
    default_attributes : dict = None

    sync_PID : int = None

    _config_file : ClassVar[str] =  f"{get_user_data_dir()}settings.yaml"
    
user_settings.load()