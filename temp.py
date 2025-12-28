import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak import BleakClient
from bleak.exc import BleakError
from bleak.backends.service import BleakGATTService
from bleak.backends.characteristic import BleakGATTCharacteristic

import time
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop  # PySide6 用の asyncio イベントループ
import sys

import Form.Views.mainWindow as MW
from Form.ViewModels.mainWindowViewModel import MainWindowViewModel
from Infrastructure.Bleak.unit_of_work_bleak import UnitOfWorkBleak
from Domain.Helper.i_message_service import IMessageService
from Domain.Helper.message_service import MessageService
#--------------------------------------------------
# デバイスをスキャンする関数
# 引数にスキャンタイムアウトを指定
async def scan_devices(scan_time_out:float=10.0):
    devices = await BleakScanner.discover(timeout = scan_time_out)  # スキャン結果を取得
    for device in devices:
        print(f"デバイス名: {device.name}, アドレス: {device.address}")

#--------------------------------------------------
# スキャンして特定のデバイスを見つける関数
# 引数にデバイス名を指定
async def get_device_by_address(address:str,scan_time_out:float=10.0)-> BLEDevice | None:
    device:BLEDevice | None = await BleakScanner.find_device_by_address(address, timeout = scan_time_out)  # スキャン結果を取得
    if device is None:
        print("デバイスは見つかりませんでした。")
        return None
    else:
        print(f"デバイス名: {device.name}, アドレス: {device.address}")
        return device
#--------------------------------------------------
# スキャンして特定のデバイスを見つける関数
# 引数にデバイス名を指定
async def scan_specific_device(target_name,target_address):
    devices = await BleakScanner.discover()
    for device in devices:
        if (device.name == target_name) & (device.address == target_address):
            print(f"特定デバイス: {device.name}, アドレス: {device.address}")
            return device
    print("特定デバイスは見つかりませんでした。")
    return None

#--------------------------------------------------
# デバイスに接続する関数
# 引数にデバイスのアドレスを指定
async def connect_to_device(device:BLEDevice):
    try:
        async with BleakClient(device, timeout=1.0) as client:
            print(f"{client.address} に接続しました。")
    except BleakError as e:
        print(f"接続エラー: {e}")
        # ここでデータの読み書きや通知の設定を行うことができます。


#--------------------------------------------------
async def connect_multiple_devices(addresses):
    tasks = [connect_to_device(address) for address in addresses]
    await asyncio.gather(*tasks)

#--------------------------------------------------
# 手動で接続する関数
# 引数にデバイスのアドレスを指定
async def manual_device_connect(device:BLEDevice,scan_time_out:float=10.0) -> BleakClient | None:
    client:BleakClient = BleakClient(device, timeout = scan_time_out)
    print(f"client : {client}")
    try:
        await client.connect()
        print(f"{device} に接続しました。")
        return client
    except BleakError as e:
        print(f"ConnectError : {e}")

#--------------------------------------------------
# 手動で切断する関数
# 引数にデバイスのアドレスを指定
async def manual_disconnect(client:BleakClient):
    if not client.is_connected:
        print(f"{client.address} は接続されていません。")
    else:
        await client.disconnect()
        print(f"{client.address} から切断しました。")

#--------------------------------------------------
# 接続状態を確認する関数
async def check_connection(device:BLEDevice):
    async with BleakClient(device) as client:
        if client.is_connected:
            print(f"{client.address} は接続されています。")
        else:
            print(f"{client.address} は接続されていません。")

#--------------------------------------------------
async def get_service(client:BleakClient,service_uuid)->BleakGATTService | None:
    try:
        for service in client.services:
            if service.uuid == service_uuid:
                print(f"サービスUUID: {service.uuid}")
                return service
    except BleakError as e:
        print(f"読み取りエラー: {e}")
#--------------------------------------------------
# 特定のキャラクタリスティックを取得する関数
# 引数にデバイスのアドレスを指定
async def get_characteristics(address):
    try:
        async with BleakClient(address) as client:
            services = client.services
            for service in services:
                print(f"サービスUUID: {service.uuid}")
                for characteristic in service.characteristics:
                    print(f"  キャラクタリスティックUUID: {characteristic.uuid}")
    except BleakError as e:
        print(f"読み取りエラー: {e}")

async def get_characteristic(service:BleakGATTService,characteristic_uuid:str)->BleakGATTCharacteristic | None:
    try:
        for characteristic in service.characteristics:
            if characteristic.uuid == characteristic_uuid:
                print(f"キャラクタリスティックUUID: {characteristic.uuid}")
                print(f"キャラクタリスティックPrp: {characteristic.properties}")
                print(f"キャラクタリスティックDesc: {characteristic.description}")
                print(f"キャラクタリスティックHandle: {characteristic.handle}")
                return characteristic
    except BleakError as e:
        print(f"読み取りエラー: {e}")
#--------------------------------------------------
# キャラクタリスティックからデータを読み取る関数
# 引数にデバイスのアドレスとキャラクタリスティックUUIDを指定
async def write_characteristic(address, characteristic_uuid, data):
    async with BleakClient(address) as client:
        await client.write_gatt_char(characteristic_uuid, data)
        print(f"キャラクタリスティック {characteristic_uuid} にデータを書き込みました。")

#--------------------------------------------------
# 通知を受信する関数
# 通知を受信するためのコールバック関数
def notification_handler(sender, data):
    # データをデコードして表示
    decoded_data = data.decode('utf-8')  # UTF-8でデコード
    print(f"通知を受信しました。デバイス: {sender}, データ: {data}")

#--------------------------------------------------
# 通知を有効化する関数
## 引数にデバイスのアドレスとキャラクタリスティックUUIDを指定
async def enable_notifications(address, characteristic_uuid):
    async with BleakClient(address) as client:
        await client.start_notify(characteristic_uuid, notification_handler)
        print(f"{characteristic_uuid} の通知を有効化しました。")

        # 通知を受信するために一定時間待機
        await asyncio.sleep(10)  # 10秒間通知を受信

#---------------------------------------------------
async def disable_notifications(address, characteristic_uuid):
    async with BleakClient(address) as client:
        await client.stop_notify(characteristic_uuid)
        print(f"{characteristic_uuid} の通知を無効化しました。")


#---------------------------------------------------
async def read_with_error_handling(address, characteristic_uuid):
    try:
        async with BleakClient(address) as client:
            data = await client.read_gatt_char(characteristic_uuid)
            print(f"データ: {data}")
    except BleakError as e:
        print(f"読み取りエラー: {e}")

#--------------------------------------------------
async def read_sensor_data(address, characteristic_uuid):
    async with BleakClient(address) as client:
        while True:
            data = await client.read_gatt_char(characteristic_uuid)
            print(f"センサーデータ: {data}")
            await asyncio.sleep(2)  # 2秒ごとにデータを取得

#--------------------------------------------------
async def control_led(address, characteristic_uuid, state):
    async with BleakClient(address) as client:
        # data = bytearray([1]) if state == "on" else bytearray([0])
        data= True
        await client.write_gatt_char(characteristic_uuid, data)
        print(f"LEDを{state}にしました。")

#--------------------------------------------------
async def communicate_with_smartphone(address, characteristic_uuid):
    async with BleakClient(address) as client:
        # スマートフォンからのデータを受信
        data = await client.read_gatt_char(characteristic_uuid)
        print(f"スマートフォンからのデータ: {data}")
        # スマートフォンにデータを送信
        response_data = bytearray([0x01])  # 例: 1バイトのデータ
        await client.write_gatt_char(characteristic_uuid, response_data)
        print("スマートフォンにデータを送信しました。")

# #--------------------------------------------------
# 通知受信時に呼ばれる関数
def notification_handler(sender, data):
    value = int.from_bytes(data, byteorder='little', signed=True)
    print(f"通知受信: {value} mA")

# 事前にペリフェラルで定義した UUID を入力してください
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef1"
WRITE_UUID    = "12345678-1234-5678-1234-56789abcdef4"
INDICATE_UUID = "12345678-1234-5678-1234-56789abcdef5"

# data_queue =asyncio.Queue()

# def handle_indicate(sender, data):
#     print(f"data : {data}")
#     data_queue.put_nowait(data)

async def get_daily_data(client:BleakClient,getDate:str):
    data_queue =asyncio.Queue()
    try:
        #データ受信待機開始
        print("Start notify")
        # data = await client.start_notify(INDICATE_UUID,handle_indicate)
        data = await client.start_notify(INDICATE_UUID,
                                        lambda sender,data:
                                        data_queue.put_nowait(data))

        #日付を送信
        strByte = getDate.encode()
        await client.write_gatt_char(WRITE_UUID,strByte)

        #受信終了チェック
        while True:
            data = await data_queue.get()
            if data == b'END':
                print("[PC] Find END -> Receive finish")
                break
            else:
                print(f"[PC] Received : {data.decode()}")

        #データ受信待機終了
        await client.stop_notify(INDICATE_UUID)
        print("End notify")
    except BleakError as e:
        print(f"BleakError : {e}")
        raise Exception(e)
    except AttributeError as e:
        print(f"AttributeError : {e}")
        raise Exception(e)
    return data_queue

def main():
    #ainWindowのviewModelの生成
    _mainWindowViewModel = MainWindowViewModel(UnitOfWorkBleak(),MessageService())
    app = QApplication(sys.argv)    # PySide6の実行
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        window = MW.MainWindow(_mainWindowViewModel)         # ユーザがコーディングしたクラス
        window.show()                   # PySide6のウィンドウを表示

        # app.aboutToQuit.connect(loop.stop)

        with loop:
            loop.run_forever()
            # sys.exit(app.exec())
    finally:        # PySide6の終了
        loop.close()
#--------------------------------------------------
async def main2():
    # target_name = "CurrentSensor_ABCD"  # スキャンするデバイス名
    # # target_address = "28:CD:C1:0F:DE:51"  # スキャンするデバイスのアドレス
    target_address = "2C:CF:67:E6:6F:94"  # スキャンするデバイスのアドレス

    # await scan_devices()
    # return

    # # スキャンを開始
    print("スキャンを開始します...")
    device: BLEDevice | None = await get_device_by_address(target_address,7.0)

    if device is None:
        print("Device is None")
        return

    try:
        client:BleakClient | None = await manual_device_connect(device)
        if client is None:
            print("Client is None")
            return
        service:BleakGATTService | None = await get_service(client,SERVICE_UUID)
        # characteristic:BleakGATTCharacteristic = await get_characteristic(service,WRITE_UUID)

        #特定日のデータを取得
        getDate:str = "20250503"
        dateData = await get_daily_data(client,getDate)

        # val = await client.read_gatt_char(WRITE_UUID)
        # print(f"キャラクタリスティック値: {val}")
        # value = int.from_bytes(val, byteorder='little', signed=True)
        # print(f"データ: {value}mA")
    except BleakError as e:
        print(f"BleakError : {e}")
    except AttributeError as e:
        print(f"AttributeError : {e}")
    finally:
        if client is not None:
            await manual_disconnect(client)

    # def detection_callback(device, adv_data):
    #     nonlocal found
    #     # print(f"デバイス名: {device.name}, アドレス: {device.address}")
    #     print(f"アドバタイズデータ: {adv_data.service_uuids}")
    #     if SERVICE_UUID.lower() in [uuid.lower() for uuid in adv_data.service_uuids]:
    #         print(f"見つかったデバイス: {device.name} ({device.address})")
    #         found = device

    # scanner = BleakScanner(detection_callback)
    # await scanner.start()
    # await asyncio.sleep(5.0)
    # await scanner.stop()

    # if found:
    #     async with BleakClient(found.address) as client:
    #         print("接続しました")
    #         await client.start_notify(CHAR_UUID, notification_handler)
    #         print("通知受信中...（10秒）")
    #         await asyncio.sleep(10)
    #         await client.stop_notify(CHAR_UUID)
    #         print("切断しました")
    # else:
    #     print("対象のデバイスが見つかりませんでした")
#--------------------------------------------------
# メイン関数
# async def main():
    # # デバイスのアドレスを指定して接続
    # asyncio.run(connect_to_device(dev.address))

    # # デバイスのアドレスを指定して接続状態を確認
    # asyncio.run(check_connection(dev.address))

    # # デバイスのアドレスを指定してキャラクタリスティックのUUIDを取得
    # asyncio.run(get_characteristics(dev.address))

    # # デバイスのアドレス、キャラクタリスティックのUUID、書き込むデータを指定
    # data_to_write = bytearray([0x01])  # 例: 1バイトのデータ
    # asyncio.run(write_characteristic("00:11:22:33:44:55", "00002a37-0000-1000-8000-00805f9b34fb", data_to_write))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定して通知を有効化
    # asyncio.run(enable_notifications(dev.address, "00002a00-0000-1000-8000-00805f9b34fb"))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定して通知を無効化
    # asyncio.run(disable_notifications(dev.address, "00002a00-0000-1000-8000-00805f9b34fb"))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定してデータを読み取る
    # asyncio.run(read_with_error_handling(dev.address, "00002a00-0000-1000-8000-00805f9b34fb"))

    # # 接続するデバイスのアドレスを指定
    # device_addresses = ["00:11:22:33:44:55", "66:77:88:99:AA:BB"]
    # asyncio.run(connect_multiple_devices(device_addresses))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定
    # asyncio.run(read_sensor_data("00:11:22:33:44:55", "00002a37-0000-1000-8000-00805f9b34fb"))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定
    # asyncio.run(control_led("00:11:22:33:44:55", "00002a37-0000-1000-8000-00805f9b34fb", "on"))

    # # デバイスのアドレスとキャラクタリスティックのUUIDを指定
    # asyncio.run(communicate_with_smartphone("00:11:22:33:44:55", "00002a37-0000-1000-8000-00805f9b34fb"))
main()
# asyncio.run(main2())