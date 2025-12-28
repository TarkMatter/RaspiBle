from Domain.Entities.log_file_entity import LogFileEntity
from Domain.Repositories.i_log_file_entities_repository import ILogFileEntitiesRepository
from Domain.shared import Shared
from Infrastructure.Helper.bleak_service import BleakService,BLEDevice

from bleak.backends.characteristic import BleakGATTCharacteristic

import asyncio,struct

class LogFileEntitiesBleak(ILogFileEntitiesRepository):
    def __init__(self):
        self._data_queue = asyncio.Queue()

    #--------------------------------------------------
    # ログファイルリスト取得用コールバック
    def callback(self,sender:BleakGATTCharacteristic,data:bytearray):
        self._data_queue.put_nowait(data)

    #--------------------------------------------------
    # ログファイルリスト取得
    async def get_log_file_list(self, address:str) ->list[LogFileEntity] | None:
        try:
            # 接続
            await BleakService.manual_connect_by_address(address)
            # 通知監視開始
            await BleakService.start_indicate_value(Shared.INDICATE_UUID,self.callback)

            # ログファイルリストを送信するように要請
            await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.GET_LOG_FILE_LIST_CONDITION)
            await asyncio.sleep(1)

            entities:list[LogFileEntity]=[]
            #受信終了チェック
            while True:
                data = await self._data_queue.get()
                if data == b'END':
                    print("[PC] Find END -> Receive finish")
                    break
                else:
                    print(f"[PC] Received : {data.decode()}")
                    entity:LogFileEntity = LogFileEntity(data.decode())
                    entities.append(entity)
            return entities

        except Exception as e:
            print("Error occured in get_log_file_list")
            raise
        finally:
            # 接続を解除
            await BleakService.manual_disconnect()

    #--------------------------------------------------
    # ログファイル取得
    async def get_log_file(self,address:str,entity:LogFileEntity):
        try:
            # 接続
            await BleakService.manual_connect_by_address(address)
            # 通知監視開始
            await BleakService.start_indicate_value(Shared.INDICATE_UUID,self.callback)

            # ログファイルリストを送信するように要請
            await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.GET_LOGS_CONDITION)
            await asyncio.sleep(1)

            #日付を送信
            strByte = (entity.file_name).encode()
            await BleakService.write_value(Shared.WRITE_UUID,strByte)

            history:list=[]
            #受信終了チェック
            while True:
                data = await self._data_queue.get()
                if data == b'END':
                    print("[PC] Find END -> Receive finish")
                    break
                else:
                    unpacked = struct.unpack("<BBBH",data)
                    print(f"[PC] Received : {unpacked}")
                    hour,minute,second,current = unpacked
                    write_data = f"{hour}:{minute}:{second},{current/100}"
                    history.append(write_data)
            return history

        except Exception as e:
            print("Error occured in get_log_file")
            raise
        finally:
            # 接続を解除
            await BleakService.manual_disconnect()
    #--------------------------------------------------
    # ログファイル削除
    async def delete_log_file(self,address:str,entity:LogFileEntity):
        try:
            # 接続
            await BleakService.manual_connect_by_address(address)
            # 通知監視開始
            await BleakService.start_indicate_value(Shared.INDICATE_UUID,self.callback)

            # ログファイルを削除するように要請
            await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.DELETE_LOG_FILE_CONDITION)
            await asyncio.sleep(1)

            byte_name = (entity.file_name).encode()
            # 値をperipheralへ書き込み
            await BleakService.write_value(Shared.WRITE_UUID,byte_name)
            # データを取得するのを待つ
            data = await asyncio.wait_for(self._data_queue.get(), timeout=3)
            # # 通知待機終了
            # await BleakService.stop_indicate_value(Shared.INDICATE_UUID)
            if data != Shared.SUCCESS_CONDITON:
                raise
        except Exception as e:
            print("Error occured in delete_log_file : {e}")
            raise
        finally:
            # 接続を解除
            await BleakService.manual_disconnect()
