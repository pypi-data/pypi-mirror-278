from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Type, List
from etiket_client.sync.database.models_pydantic import sync_item, new_sync_item

class SyncSourceAbstract(ABC):
    @property
    @abstractmethod
    def SyncAgentName(self) -> str:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def ConfigDataClass(self) -> Type[dataclass]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def MapToASingleScope(self) -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def getNewDatasets(configData: Type[dataclass], lastIdentifier : str) -> 'List[new_sync_item] | None':
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def checkLiveDataset(configData: Type[dataclass], syncIdentifier : sync_item) -> bool:
        pass
    
    @staticmethod
    @abstractmethod
    def syncDatasetNormal(configData: Type[dataclass], syncIdentifier : sync_item):
        pass
    
    @staticmethod
    @abstractmethod
    def syncDatasetLive(configData: Type[dataclass], syncIdentifier : sync_item):
        pass
    
    # TODO add method to detect changes in old files -- files that have already been synchronized.
    