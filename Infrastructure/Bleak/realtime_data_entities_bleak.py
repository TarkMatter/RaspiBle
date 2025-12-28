from typing import List
from Domain.Entities.realtime_data_entity import RealTimeDataEntity
from Domain.Repositories.i_realtime_date_entities_repository import IRealTimeDataEntitiesRepository
from Domain.shared import Shared
from Infrastructure.Helper.bleak_service import BleakService
from bleak.backends.characteristic import BleakGATTCharacteristic

import time
import asyncio

# GET_CONDITION_UUID="12345678-1234-5678-1234-56789abcdef3"
# INDICATE_UUID = "12345678-1234-5678-1234-56789abcdef5"

# PING_SEND_DURATION = 8
# START_CONDITION = b'NowCurrent'
# END_CONDITON = b'END'
# CONTINUE_CONDITION = b'PING'

class RealTimeDataEntitiesBleak(IRealTimeDataEntitiesRepository):
    def __init__(self):
        self.SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef1"
        self._getdata:bytearray | None = None
        self._data_queue = asyncio.Queue()
        self._ping_send_task:asyncio.Task

    #--------------------------------------------------
    def callback(self,sender:BleakGATTCharacteristic,data:bytearray):
        current_value = int.from_bytes(data,byteorder="little")
        self._data_queue.put_nowait(current_value)

    #--------------------------------------------------
    async def connect(self, address: str):
        try:
            await BleakService.manual_connect_by_address(address)
            await BleakService.start_indicate_value(Shared.INDICATE_UUID,self.callback)

            #現在電流値を通知するように要請
            await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.GET_CURRENT_START_CONDITION)
            # await BleakService.write_value('12345678-1234-5678-1234-56789abcdef3',b"NowCurrent")
            self._ping_send_task = asyncio.create_task(self._periodic_writer())
            print("Send notify command ...")
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Connect Error : {e}")

    #--------------------------------------------------
    async def cancel_notify(self):
        #現在電流値を通知するように要請
        await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.END_CONDITON)
        print("Send notify finish command ...")
        await asyncio.sleep(0.1)

    #--------------------------------------------------
    async def get_now_data(self) ->RealTimeDataEntity | None:
        try:
            data = await asyncio.wait_for(self._data_queue.get(), timeout=5)

            return RealTimeDataEntity(time.localtime(),data/100)

        except asyncio.TimeoutError as e:
            print("通知を待機中にタイムアウトしました")
            raise

        except Exception as e:
            print(f"データ取得エラー: {e}")
            return None

    #--------------------------------------------------
    async def close(self):
        if self._ping_send_task:
            self._ping_send_task.cancel()
            try:
                # キャンセルされたタスクが終了するまで待機
                await self._ping_send_task
            except asyncio.CancelledError:
                print("[Pico] _ping_send_task cancelled")

        await BleakService.stop_indicate_value(Shared.INDICATE_UUID)
        await self._disconnect()
        return

    #--------------------------------------------------
    async def _disconnect(self):
        if BleakService.is_client_connected:
            await BleakService.manual_disconnect()

    #--------------------------------------------------
    async def _periodic_writer(self):
        try:
            while True:
                print(">> Send continue condition :", Shared.CONTINUE_CONDITION)
                await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.CONTINUE_CONDITION)
                await asyncio.sleep(Shared.PING_SEND_DURATION)
        except asyncio.CancelledError:
            print("Periodic writer cancelled.")
        except Exception as e:
            print("Error during periodic write:", e)

        # device: BLEDevice = None
        # client:BleakClient = None
        # # service:BleakGATTService = None
        # realtime_data:RealTimeDataEntity = None

        # device = await BleakService.get_device_by_address(address)


        # if device is None:
        #     print("Device is None")
        #     raise Exception("Device is None")

        # try:
        #     client = await BleakService.manual_device_connect(device)
        #     if client is None:
        #         print("Client is None")
        #         raise Exception("Device is None")

        #     # service = await BleakService.get_service(client,self.SERVICE_UUID)
        #     # characteristic:BleakGATTCharacteristic = await get_characteristic(service,WRITE_UUID)

        #     #特定日のデータを取得
        #     # getDate:str = "20250503"
        #     # dateData = await get_daily_data(client,getDate)
        #     # realtime_data:RealTimeDataEntity = RealTimeDataEntity(time.localtime(),124.3)
        #     realtime_data = await BleakService.get_test_data(client)

        #     # val = await client.read_gatt_char(WRITE_UUID)
        #     # print(f"キャラクタリスティック値: {val}")
        #     # value = int.from_bytes(val, byteorder='little', signed=True)
        #     # print(f"データ: {value}mA")
        #     return realtime_data
        # except asyncio.CancelledError as e:
        #     print(f"asyncio.cancelledError : {e}")
        #     raise
        # except BleakError as e:
        #     print(f"BleakError : {e}")
        # except AttributeError as e:
        #     print(f"AttributeError : {e}")
        # except Exception as e:
        #     print(f"Exception in get_now_data method: {e}")
        # finally:
        #     if client is not None:
        #         await BleakService.manual_disconnect(client)
