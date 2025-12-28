from abc import ABCMeta, abstractmethod

from Domain.Entities.current_time_entity import CurrentTimeEntity
class ICurrentTimeEntitiesRepository(metaclass=ABCMeta):
    """
    Interface for the CurrentTimeEntity repository.
    """
    @abstractmethod
    async def send_current_time(self, address:str,entity: CurrentTimeEntity):
        raise NotImplementedError("send_current_time method must be implemented")