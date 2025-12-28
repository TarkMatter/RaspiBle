from abc import ABCMeta, abstractmethod

from Domain.Entities.log_file_entity import LogFileEntity
class ILogFileEntitiesRepository(metaclass=ABCMeta):
    """
    Interface for the CurrentTimeEntity repository.
    """
    @abstractmethod
    async def get_log_file_list(self, address:str) -> LogFileEntity:
        raise NotImplementedError("get_log_file_list method must be implemented")

    @abstractmethod
    async def get_log_file(self, address:str,entity:LogFileEntity):
        raise NotImplementedError("get_log_file method must be implemented")

    @abstractmethod
    async def delete_log_file(self, address:str,entity:LogFileEntity):
        raise NotImplementedError("delete_log_file method must be implemented")