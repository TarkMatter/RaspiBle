from Domain.Repositories.i_unit_of_work import IUnitOfWork
from Domain.Repositories.i_current_time_entities_repository import ICurrentTimeEntitiesRepository
from Domain.Repositories.i_log_file_entities_repository import ILogFileEntitiesRepository
from Domain.Repositories.i_peripheral_entities_repository import IPeripheralEntitiesRepository
from Domain.Repositories.i_realtime_date_entities_repository import IRealTimeDataEntitiesRepository
from Infrastructure.factories import Factories

class UnitOfWorkBleak(IUnitOfWork):
    def __init__(self):
        pass
        # self._peripheral_entities_repository = None

    @property
    def current_time_entities_repository(self) -> ICurrentTimeEntitiesRepository:
        return Factories.create_current_time_entities_repository()

    @property
    def log_file_entities_repository(self) -> ILogFileEntitiesRepository:
        return Factories.create_log_file_entities_repository()

    @property
    def peripheral_entities_repository(self) -> IPeripheralEntitiesRepository:
        return Factories.create_peripheral_entities_repository()

    @property
    def realtime_data_entities_repository(self) -> IRealTimeDataEntitiesRepository:
        return Factories.create_realtime_data_entities_repository()