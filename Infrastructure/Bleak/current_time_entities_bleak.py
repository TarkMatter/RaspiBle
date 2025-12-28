from typing import List
from Domain.Entities.current_time_entity import CurrentTimeEntity
from Domain.shared import Shared
from Domain.Repositories.i_current_time_entities_repository import ICurrentTimeEntitiesRepository
from Infrastructure.Helper.bleak_service import BleakService

from bleak.backends.characteristic import BleakGATTCharacteristic

import asyncio
from datetime import datetime

class CurrentTimeEntitiesBleak(ICurrentTimeEntitiesRepository):
    def __init__(self):
        self._data_queue = asyncio.Queue()

    #--------------------------------------------------
    # 通知データの取得コールバック
    def callback(self,sender:BleakGATTCharacteristic,data:bytearray):
        self._data_queue.put_nowait(data)

    #--------------------------------------------------
    # 現在値の送信
    async def send_current_time(self,address:str,entity:CurrentTimeEntity):
        try:
            # 接続開始
            await BleakService.manual_connect_by_address(address)
            # 通知待機開始
            await BleakService.start_indicate_value(Shared.INDICATE_UUID,self.callback)

            #現在時刻を取得するように要請
            await BleakService.write_value(Shared.GET_CONDITION_UUID,Shared.CATCH_CURRENT_TIME_CONDITION)
            await asyncio.sleep(1)

            # 現在時刻を取得
            current_time:datetime = datetime.now()
            # 形式を変更
            send_data = current_time.strftime('%Y/%m/%d/%H/%M/%S')
            # エンコード
            byte_data = send_data.encode()
            # 値をperipheralへ書き込み
            await BleakService.write_value(Shared.WRITE_UUID,byte_data)
            # データを取得するのを待つ
            data = await asyncio.wait_for(self._data_queue.get(), timeout=3)
            # 通知待機終了
            await BleakService.stop_indicate_value(Shared.INDICATE_UUID)
            if data != Shared.SUCCESS_CONDITON:
                raise
        except Exception as e:
            raise
        finally:
            # 接続解除
            await BleakService.manual_disconnect()
