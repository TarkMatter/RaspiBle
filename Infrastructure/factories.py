from dataclasses import dataclass

from Infrastructure.Bleak.current_time_entities_bleak import CurrentTimeEntitiesBleak
from Infrastructure.Bleak.log_file_entities_bleak import LogFileEntitiesBleak
from Infrastructure.Bleak.realtime_data_entities_bleak import RealTimeDataEntitiesBleak
from Infrastructure.Bleak.peripheral_entities_bleak import PeripheralEntitiesBleak

@dataclass
class Factories:
    _current_time_entities_repository:CurrentTimeEntitiesBleak = None
    _log_file_entities_repository:LogFileEntitiesBleak = None
    _peripheral_entities_repository:PeripheralEntitiesBleak = None
    _realtime_data_entities_repository:RealTimeDataEntitiesBleak = None

    def __init__(self):
        pass

    @classmethod
    def create_current_time_entities_repository(cls)-> CurrentTimeEntitiesBleak:
        if cls._current_time_entities_repository is None:
            cls._current_time_entities_repository = CurrentTimeEntitiesBleak()
        return cls._current_time_entities_repository
    
    @classmethod
    def create_log_file_entities_repository(cls)-> LogFileEntitiesBleak:
        if cls._log_file_entities_repository is None:
            cls._log_file_entities_repository = LogFileEntitiesBleak()
        return cls._log_file_entities_repository

    @classmethod
    def create_peripheral_entities_repository(cls)-> PeripheralEntitiesBleak:
        if cls._peripheral_entities_repository is None:
            cls._peripheral_entities_repository = PeripheralEntitiesBleak()
        return cls._peripheral_entities_repository

    @classmethod
    def create_realtime_data_entities_repository(cls)-> RealTimeDataEntitiesBleak:
        if cls._realtime_data_entities_repository is None:
            cls._realtime_data_entities_repository = RealTimeDataEntitiesBleak()
        return cls._realtime_data_entities_repository

    # @staticmethod
    # def CreateItemCodeEntitiesRepository(context:DbContext)-> ItemCodeEntitiesSqlite:
    #     return ItemCodeEntitiesSqlite(context)

    # @property
    # def CreateDimensionValueEntitiesRepository(self,context:DbContext)-> DimensionValueEntitiesSqlite:
    #     return DimensionValueEntitiesSqlite(context)


    # @property
    # def CreateEmployeeEntitiesRepository(self,context:DbContext)-> EmployeeEntitiesSqlite:
    #     return EmployeeEntitiesSqlite(context)
    


    
    # @property
    # def CreateAppearanceEntitiesRepository(self,context:DbContext)-> AppearanceEntitiesSqlite:
    #     return AppearanceEntitiesSqlite(context)