from typing import List
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak import BleakClient
from bleak.exc import BleakError
from bleak.backends.service import BleakGATTService

from typing import Callable

from dataclasses import dataclass

@dataclass
class BleakService():
    _device:BLEDevice | None = None
    _client:BleakClient | None = None

    #--------------------------------------------------
    # デバイスをスキャンする関数
    # 引数にスキャンタイムアウトを指定
    @classmethod
    async def scan_devices(cls,scan_time_out:float=10.0) -> List[BLEDevice]:
        print("Start scanning ...")
        return await BleakScanner.discover(timeout = scan_time_out)  # スキャン結果を取得

    #--------------------------------------------------
    # スキャンして特定のデバイスを見つける関数
    # 引数にデバイス名を指定
    @classmethod
    async def get_device_by_address(cls,address:str,scan_time_out:float=10.0):
        cls._device = await BleakScanner.find_device_by_address(address, timeout = scan_time_out)  # スキャン結果を取得
        if cls._device is None:
            print("デバイスは見つかりませんでした。")
        else:
            print(f"デバイス名: {cls._device.name}, アドレス: {cls._device.address}")

    #--------------------------------------------------
    # 手動で接続する関数
    # 引数にデバイスのアドレスを指定
    @classmethod
    async def manual_device_connect(cls,scan_time_out:float=10.0):
        if cls._device is None:
            print("BLEデバイスが取得できていません")
            return

        cls._client = BleakClient(cls._device, timeout = scan_time_out)
        print(f"client : {cls._client}")
        try:
            await cls._client.connect()
            print(f"{cls._device} に接続しました。")
        except BleakError as e:
            print(f"ConnectError : {e}")

    #--------------------------------------------------
    #clientに接続されているか判定
    @classmethod
    def is_client_connected(cls) -> bool:
        if cls._client is None:
            return False
        return cls._client.is_connected

    #--------------------------------------------------
    @classmethod
    async def manual_connect_by_address(cls,address:str,scan_time_out:float=10.0):
        try:
            #デバイスの取得
            if cls._device is not None:
                print("既にデバイスを取得しています")
            else:
                cls._device = await BleakScanner.find_device_by_address(address, timeout = scan_time_out)
                if cls._device is None:
                    raise Exception("デバイスは見つかりませんでした")

                print(f"デバイス名: {cls._device.name}, アドレス: {cls._device.address}")

            #クライアントの作成
            if cls._client is not None:
                print("既にクライアントは作成されています")
            else:
                cls._client = BleakClient(cls._device, timeout = scan_time_out)
                if cls._client is None:
                    raise Exception("クライアントを作成できませんでした")

                print(f"client : {cls._client}")

            #接続
            if cls._client.is_connected:
                print("既に接続されています")
            else:
                await cls._client.connect()
                print(f"{cls._device} に接続しました。")

        except BleakError as e:
            print(f"ConnectError : {e}")
            raise

    #--------------------------------------------------
    # 手動で切断する関数
    # 引数にデバイスのアドレスを指定
    @classmethod
    async def manual_disconnect(cls):
        if cls._device is None:
            print("BLEデバイスが取得できていません")
            return
        if cls._client is None:
            print("BLEclientが作成されていません")
            return

        if not cls._client.is_connected:
            print(f"{cls._client.address} は接続されていません。")
        else:
            await cls._client.disconnect()
            print(f"{cls._client.address} から切断しました。")

        cls._client = None
        cls._device = None

    #--------------------------------------------------
    #サービスを取得
    @classmethod
    async def get_service(cls,service_uuid)->BleakGATTService | None:
        if cls._device is None:
            print("BLEデバイスが取得できていません")
            return

        if cls._client is None:
            print("BLEclientが作成されていません")
            return

        if not cls._client.is_connected:
            print(f"{cls._client.address} は接続されていません。")
        try:
            for service in cls._client.services:
                if service.uuid == service_uuid:
                    print(f"サービスUUID: {service.uuid}")
                    return service
        except BleakError as e:
            print(f"読み取りエラー: {e}")

    #--------------------------------------------------
    @classmethod
    async def get_Value(cls,uuid:str) -> bytearray:
        if cls._client is None:
            return bytearray()
        return await cls._client.read_gatt_char(uuid)

    #--------------------------------------------------
    @classmethod
    async def start_indicate_value(cls,uuid:str,callback:Callable):
        print("start notify...")
        if cls._client is None:
            return
        await cls._client.start_notify(uuid,callback)

    #--------------------------------------------------
    @classmethod
    async def stop_indicate_value(cls,uuid:str):
        print("finish notify !")
        if cls._client is None:
            return
        if cls._client.is_connected:
            await cls._client.stop_notify(uuid)

    #--------------------------------------------------
    @classmethod
    async def write_value(cls,uuid:str,byteData:bytearray):
        if cls._client is None:
            return bytearray()
        await cls._client.write_gatt_char(uuid,byteData)