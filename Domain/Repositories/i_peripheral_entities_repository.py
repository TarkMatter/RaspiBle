from abc import ABCMeta, abstractmethod

from Domain.Entities.peripheral_entity import PeripheralEntity
class IPeripheralEntitiesRepository(metaclass=ABCMeta):
    """
    Interface for the ApPeripheralEntity repository.
    """

    @abstractmethod
    def get_all_entities(self) ->list[PeripheralEntity] | None:
        raise NotImplementedError("get_all_entities method must be implemented")