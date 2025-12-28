from abc import ABCMeta,abstractmethod
from Domain.Repositories.i_current_time_entities_repository import ICurrentTimeEntitiesRepository
from Domain.Repositories.i_log_file_entities_repository import ILogFileEntitiesRepository
from Domain.Repositories.i_peripheral_entities_repository import IPeripheralEntitiesRepository
from Domain.Repositories.i_realtime_date_entities_repository import IRealTimeDataEntitiesRepository

class IUnitOfWork(metaclass=ABCMeta):
    @property
    @abstractmethod
    def current_time_entities_repository(self) -> ICurrentTimeEntitiesRepository:
        raise NotImplementedError("CurrentTimeEntitiesRepository property must be implemented")
    
    @property
    @abstractmethod
    def log_file_entities_repository(self) -> ILogFileEntitiesRepository:
        raise NotImplementedError("log_file_entities_repository property must be implemented")

    @property
    @abstractmethod
    def peripheral_entities_repository(self) -> IPeripheralEntitiesRepository:
        raise NotImplementedError("ItemCodeEntitiesRepository property must be implemented")

    @property
    @abstractmethod
    def realtime_data_entities_repository(self) -> IRealTimeDataEntitiesRepository:
        raise NotImplementedError("RealTimeEntitiesRepository property must be implemented")