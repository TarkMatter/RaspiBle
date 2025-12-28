from abc import ABCMeta, abstractmethod

from Domain.Entities.realtime_data_entity import RealTimeDataEntity
class IRealTimeDataEntitiesRepository(metaclass=ABCMeta):
    """
    Interface for the RealTimeDataEntity repository.
    """
    @abstractmethod
    async def connect(self, address: str):
        raise NotImplementedError("connect method must be implemented")

    @abstractmethod
    async def _disconnect(self):
        raise NotImplementedError("disconnect method must be implemented")

    @abstractmethod
    async def close(self):
        raise NotImplementedError("close method must be implemented")

    @abstractmethod
    def get_now_data(self,address:str) ->RealTimeDataEntity | None:
        raise NotImplementedError("get_now_data method must be implemented")

    @abstractmethod
    async def cancel_notify(self):
        raise NotImplementedError("cancel_notify method must be implemented")