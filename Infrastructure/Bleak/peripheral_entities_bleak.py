from typing import List
from Domain.Entities.peripheral_entity import PeripheralEntity
from Domain.Repositories.i_peripheral_entities_repository import IPeripheralEntitiesRepository
from Infrastructure.Helper.bleak_service import BleakService,BLEDevice

class PeripheralEntitiesBleak(IPeripheralEntitiesRepository):
    def __init__(self):
        pass
    #--------------------------------------------------
    # 周辺のperipheral一覧の取得
    async def get_all_entities(self) -> list[PeripheralEntity] | None:
        devices:List[BLEDevice] = await BleakService.scan_devices()
        entities:List[PeripheralEntity] = []
        for device in devices:
            entities.append(PeripheralEntity(device.name,device.address))
        return entities
