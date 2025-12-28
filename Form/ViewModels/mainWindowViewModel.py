from Domain.Entities.current_time_entity import CurrentTimeEntity
from Domain.Entities.log_file_entity import LogFileEntity
from Domain.Entities.peripheral_entity import PeripheralEntity
from Domain.Entities.realtime_data_entity import RealTimeDataEntity
from Domain.Repositories.i_unit_of_work import IUnitOfWork
from Domain.Helper.i_message_service import IMessageService
from Form.ListModels.peripheral_list_model import PeripheralListModel
from Form.ListModels.log_file_list_model import LogFileListModel
import asyncio,datetime

from PySide6.QtCore import Signal,QObject,QItemSelection
from PySide6.QtWidgets import QMessageBox,QFileDialog

from enum import Enum
import os

SEARCH_BUTTON_NAME_WAITING = "周辺検索"
SEARCH_BUTTON_NAME_SEARCHING = "検索中……"

GET_DATA_BUTTON_NAME_WAITING = "現在値取得"
GET_DATA_BUTTON_NAME_CONNECTING = "接続中……"
GET_DATA_BUTTON_NAME_GETTING = "取得中…"
GET_DATA_BUTTON_NAME_DISCONNECTING = "切断中……"

SET_TIME_BUTTON_NAME_SETTING = "設定中……"
SET_TIME_BUTTON_NAME_WAITING = "現在時刻設定"

GET_LOG_FILE_BUTTON_NAME_WAITING = "リスト取得"
GET_LOG_FILE_BUTTON_NAME_GETTING = "取得中..."

GET_LOG_BUTTON_NAME_WAITING = "ログ取得"
GET_LOG_BUTTON_NAME_GETTING = "取得中..."

DELETE_LOG_BUTTON_NAME_WAITING = "ログ削除"
DELETE_LOG_BUTTON_NAME_GETTING = "削除中..."


class ConnectState(Enum):
    TO_CONNECTING = 0
    TO_GETTING = 1
    TO_DISCONNECTING = 2
    TO_WAITING = 3

EXIT_BUTTON_NAME = "終了"

class MainWindowViewModel(QObject):
    #Signal
    #現在の電流値
    current_value:Signal= Signal(RealTimeDataEntity)
    current_value_text:Signal = Signal(str)

    # Peripheralリスト
    _peripheral_list_model:PeripheralListModel = PeripheralListModel()
    # logfileリスト
    _log_file_list_model:LogFileListModel = LogFileListModel()

    #検索ボタン：プロパティ
    search_button_text:Signal = Signal(str)
    search_button_enable:Signal = Signal(bool)

    #peripheralリスト：プロパティ
    peripheral_list_enable:Signal = Signal(bool)

    #対象Peripheral名ラベル：プロパティ
    target_label_text:Signal = Signal(str)

    #現在値取得ボタン：プロパティ
    get_data_button_text:Signal = Signal(str)
    get_data_button_enable:Signal = Signal(bool)

    #終了ボタン：プロパティ
    exit_button_enable:Signal = Signal(bool)

    #ログファイルリスト取得ボタン：プロパティ
    get_log_file_list_button_text:Signal = Signal(str)
    get_log_file_list_button_enable:Signal = Signal(bool)

    # logfileリスト：プロパティ
    log_file_list_enable:Signal = Signal(bool)

    # ログ取得ボタン：プロパティ
    get_log_file_button_text:Signal = Signal(str)
    get_log_file_button_enable:Signal = Signal(bool)

    # ログ削除ボタン：プロパティ
    delete_log_file_button_text:Signal = Signal(str)
    delete_log_file_button_enable:Signal = Signal(bool)

    #時刻設定ボタン：プロパティ
    set_time_button_text:Signal = Signal(str)
    set_time_button_enable:Signal = Signal(bool)

    # 出力フォルダテキストボックス：プロパティ
    output_folder_qLineEdit_text:Signal = Signal(str)
    output_folder_qLineEdit_enable:Signal = Signal(bool)

    # フォルダ選択ボタン：プロパティ
    folder_select_button_text:Signal = Signal(str)
    folder_select_button_enable:Signal = Signal(bool)

    #アプリケーション終了通知
    request_exit:Signal = Signal()

    _save_path:str = ""

    _selected_peripheral_entity:PeripheralEntity = None
    _selected_log_file_entity:LogFileEntity = None
    _getdata_task:asyncio.Task = None

    _getting_data = False

    @property
    def title(self):
        return self._title

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def is_visible(self):
        return self._is_visible

    def show(self):
        self._is_visible = True

    def hide(self):
        self._is_visible = False

    #--------------------------------------------------
    #コンストラクタ
    def __init__(self,unit_of_work:IUnitOfWork,message_service:IMessageService):
        super().__init__()
        self._unit_of_work:IUnitOfWork = unit_of_work
        self._message_service:IMessageService = message_service

        self._title = "Main Window"
        self._width = 800
        self._height = 600
        self._is_visible = True

    #--------------------------------------------------
    #検索ボタン処理-UI変更
    def _change_button_display_on_search(self,searching:bool):
        if searching:
            self.search_button_text.emit(SEARCH_BUTTON_NAME_SEARCHING)
        else:
            self.search_button_text.emit(SEARCH_BUTTON_NAME_WAITING)

        self.search_button_enable.emit(not searching) # 検索ボタン
        self.peripheral_list_enable.emit(not searching) # 周辺機器リスト
        self.get_data_button_enable.emit(not searching) # 現在値取得ボタン
        self.log_file_list_enable.emit(not searching) # ログリスト
        self.get_log_file_list_button_enable.emit(not searching) # ログファイルリスト取得ボタン
        self.get_log_file_button_enable.emit(not searching) # ログ取得ボタン
        self.delete_log_file_button_enable.emit(not searching) # ログ削除ボタン
        self.output_folder_qLineEdit_enable.emit(not searching) # パステキストボックス
        self.folder_select_button_enable.emit(not searching) # フォルダ選択ボタン
        self.set_time_button_enable.emit(not searching) # 時刻設定ボタン
        self.exit_button_enable.emit(not searching) # 終了ボタン

    #--------------------------------------------------
    #現在値取得ボタン処理-UI変更
    def _change_button_display_on_getting(self,nextState:int):
        match nextState:
            case ConnectState.TO_CONNECTING:
                self.get_data_button_text.emit(GET_DATA_BUTTON_NAME_CONNECTING)
                self.search_button_enable.emit(False) # 検索ボタン
                self.peripheral_list_enable.emit(False) # 周辺機器リスト
                self.get_data_button_enable.emit(False) # 現在値取得ボタン
                self.log_file_list_enable.emit(False) # ログリスト
                self.get_log_file_list_button_enable.emit(False) # ログファイルリスト取得ボタン
                self.get_log_file_button_enable.emit(False) # ログ取得ボタン
                self.delete_log_file_button_enable.emit(False) # ログ削除ボタン
                self.output_folder_qLineEdit_enable.emit(False) # パステキストボックス
                self.folder_select_button_enable.emit(False) # フォルダ選択ボタン
                self.set_time_button_enable.emit(False) # 時刻設定ボタン
                self.exit_button_enable.emit(False) # 終了ボタン

            case ConnectState.TO_GETTING:
                self.get_data_button_text.emit(GET_DATA_BUTTON_NAME_GETTING)
                self.get_data_button_enable.emit(True) # 現在値取得ボタン

            case ConnectState.TO_DISCONNECTING:
                self.get_data_button_text.emit(GET_DATA_BUTTON_NAME_DISCONNECTING)
                self.get_data_button_enable.emit(False) # 現在値取得ボタン

            case ConnectState.TO_WAITING:
                self.get_data_button_text.emit(GET_DATA_BUTTON_NAME_WAITING)
                self.search_button_enable.emit(True) # 検索ボタン
                self.peripheral_list_enable.emit(True) # 周辺機器リスト
                self.get_data_button_enable.emit(True) # 現在値取得ボタン
                self.log_file_list_enable.emit(True) # ログリスト
                self.get_log_file_list_button_enable.emit(True) # ログファイルリスト取得ボタン
                self.get_log_file_button_enable.emit(True) # ログ取得ボタン
                self.delete_log_file_button_enable.emit(True) # ログ削除ボタン
                self.output_folder_qLineEdit_enable.emit(True) # パステキストボックス
                self.folder_select_button_enable.emit(True) # フォルダ選択ボタン
                self.set_time_button_enable.emit(True) # 時刻設定ボタン
                self.exit_button_enable.emit(True) # 終了ボタン

    #--------------------------------------------------
    #現在時刻設定ボタン処理-UI変更
    def _change_button_display_on_set_time(self,setting:bool):
        if setting:
            self.set_time_button_text.emit(SET_TIME_BUTTON_NAME_SETTING)
        else:
            self.set_time_button_text.emit(SET_TIME_BUTTON_NAME_WAITING)

        self.search_button_enable.emit(not setting) # 検索ボタン
        self.peripheral_list_enable.emit(not setting) # 周辺機器リスト
        self.get_data_button_enable.emit(not setting) # 現在値取得ボタン
        self.log_file_list_enable.emit(not setting) # ログリスト
        self.get_log_file_list_button_enable.emit(not setting) # ログファイルリスト取得ボタン
        self.get_log_file_button_enable.emit(not setting) # ログ取得ボタン
        self.delete_log_file_button_enable.emit(not setting) # ログ削除ボタン
        self.output_folder_qLineEdit_enable.emit(not setting) # パステキストボックス
        self.folder_select_button_enable.emit(not setting) # フォルダ選択ボタン
        self.set_time_button_enable.emit(not setting) # 時刻設定ボタン
        self.exit_button_enable.emit(not setting) # 終了ボタン

    #--------------------------------------------------
    #ログファイルリスト取得ボタン処理-UI変更
    def _change_button_display_on_log_file_list(self,getting:bool):
        if getting:
            self.get_log_file_list_button_text.emit(GET_LOG_FILE_BUTTON_NAME_GETTING)
        else:
            self.get_log_file_list_button_text.emit(GET_LOG_FILE_BUTTON_NAME_WAITING)

        self.search_button_enable.emit(not getting) # 検索ボタン
        self.peripheral_list_enable.emit(not getting) # 周辺機器リスト
        self.get_data_button_enable.emit(not getting) # 現在値取得ボタン
        self.log_file_list_enable.emit(not getting) # ログリスト
        self.get_log_file_list_button_enable.emit(not getting) # ログファイルリスト取得ボタン
        self.get_log_file_button_enable.emit(not getting) # ログ取得ボタン
        self.delete_log_file_button_enable.emit(not getting) # ログ削除ボタン
        self.output_folder_qLineEdit_enable.emit(not getting) # パステキストボックス
        self.folder_select_button_enable.emit(not getting) # フォルダ選択ボタン
        self.set_time_button_enable.emit(not getting) # 時刻設定ボタン
        self.exit_button_enable.emit(not getting) # 終了ボタン

    #--------------------------------------------------
    #ログ取得ボタン処理-UI変更
    def _change_button_display_on_get_log_file(self,getting:bool):
        if getting:
            self.get_log_file_button_text.emit(GET_LOG_BUTTON_NAME_GETTING)
        else:
            self.get_log_file_button_text.emit(GET_LOG_BUTTON_NAME_WAITING)

        self.search_button_enable.emit(not getting) # 検索ボタン
        self.peripheral_list_enable.emit(not getting) # 周辺機器リスト
        self.get_data_button_enable.emit(not getting) # 現在値取得ボタン
        self.log_file_list_enable.emit(not getting) # ログリスト
        self.get_log_file_list_button_enable.emit(not getting) # ログファイルリスト取得ボタン
        self.get_log_file_button_enable.emit(not getting) # ログ取得ボタン
        self.delete_log_file_button_enable.emit(not getting) # ログ削除ボタン
        self.output_folder_qLineEdit_enable.emit(not getting) # パステキストボックス
        self.folder_select_button_enable.emit(not getting) # フォルダ選択ボタン
        self.set_time_button_enable.emit(not getting) # 時刻設定ボタン
        self.exit_button_enable.emit(not getting) # 終了ボタン

    #--------------------------------------------------
    #ログ削除ボタン処理-UI変更
    def _change_button_display_on_delete_log_file(self,getting:bool):
        if getting:
            self.delete_log_file_button_text.emit(DELETE_LOG_BUTTON_NAME_GETTING)
        else:
            self.delete_log_file_button_text.emit(DELETE_LOG_BUTTON_NAME_WAITING)

        self.search_button_enable.emit(not getting) # 検索ボタン
        self.peripheral_list_enable.emit(not getting) # 周辺機器リスト
        self.get_data_button_enable.emit(not getting) # 現在値取得ボタン
        self.log_file_list_enable.emit(not getting) # ログリスト
        self.get_log_file_list_button_enable.emit(not getting) # ログファイルリスト取得ボタン
        self.get_log_file_button_enable.emit(not getting) # ログ取得ボタン
        self.delete_log_file_button_enable.emit(not getting) # ログ削除ボタン
        self.output_folder_qLineEdit_enable.emit(not getting) # パステキストボックス
        self.folder_select_button_enable.emit(not getting) # フォルダ選択ボタン
        self.set_time_button_enable.emit(not getting) # 時刻設定ボタン
        self.exit_button_enable.emit(not getting) # 終了ボタン

    #--------------------------------------------------
    #検索ボタン押下処理
    async def search_button_execute(self):
        #ボタンラベル名を検索中のものに変更
        self._change_button_display_on_search(True)
        try:
            #ターゲットラベルのクリア
            self.target_label_text.emit("")

            #周辺機器を検索
            devices:list[PeripheralEntity] = await self._unit_of_work.peripheral_entities_repository.get_all_entities()

            #リストをクリア
            self._peripheral_list_model.clear()

            #機器が見つからなければ終了
            if devices is None:
                print("データが取得できませんでした")
                self._message_service.show_error("データが取得できませんでした","データ取得エラー")
                return

            #リストに取得機器名を登録
            for device in devices:
                print(f"{device.device_name} / {device.mac_address}")
                self._peripheral_list_model.add_item(device)
        finally:
            #ボタンラベル名を元に戻る
            self._change_button_display_on_search(False)

    #--------------------------------------------------
    #Peripheralリスト選択変更時
    def peripheral_list_view_selectionChanged(self,selected:QItemSelection,deselected:QItemSelection):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            self._selected_peripheral_entity = self._peripheral_list_model.get(index)
            self.target_label_text.emit(self._selected_peripheral_entity.display_peripheral_name)

    #--------------------------------------------------
    #現在値取得ボタン押下処理
    def get_data_button_execute(self):
        if self._selected_peripheral_entity is None:
                self._message_service.show_error("接続対象が選択されていません","対象不定")
                return

        try:
            if not self._getting_data:
                print("Getting start ...")
                self._getting_data = True
                self._change_button_display_on_getting(ConnectState.TO_CONNECTING)

                if self._getdata_task is not None and not self._getdata_task.done():
                    self._getdata_task.cancel()

                self._getdata_task = asyncio.create_task(self._start_realtime_data_loop())
            else:
                print("Getting finish !")
                self._getting_data = False
                self._change_button_display_on_getting(ConnectState.TO_DISCONNECTING)
                if self._getdata_task:
                    self._getdata_task.cancel()
        except UnboundLocalError as e:
            print(f"UnboundLocalError in get_data_button_execute method : {e}")
        except Exception as e:
            print(f"Exception in get_data_button_execute method : {e}")

    #--------------------------------------------------
    async def _start_realtime_data_loop(self):
        try:
            #接続～indicate開始
            await self._unit_of_work.realtime_data_entities_repository.connect(self._selected_peripheral_entity.mac_address)

            await asyncio.sleep(0.5)

            self._change_button_display_on_getting(ConnectState.TO_GETTING)

            #データ受信
            while self._getting_data:
                realtime_data:RealTimeDataEntity = await self._unit_of_work.realtime_data_entities_repository.get_now_data()
                if realtime_data:
                    # self.current_value.emit(realtime_data)
                    self.current_value_text.emit(f"{realtime_data.current:.2f}A")
                else:
                    print("データが取得できませんでした")
                    self._getting_data = False
                    await self._unit_of_work.realtime_data_entities_repository.cancel_notify()
                    raise Exception()
                await asyncio.sleep(1)
        except asyncio.TimeoutError as e:
            print(f"timeout error : {e}")
            self._getting_data = False

        except asyncio.CancelledError:
            await self._unit_of_work.realtime_data_entities_repository.cancel_notify()
            print("キャンセルされました")

        except Exception as e:
            print(f"Can't get data : {e}")
        finally:
            #接続を切断
            await self._unit_of_work.realtime_data_entities_repository.close()

            await asyncio.sleep(0.5)

            self.current_value_text.emit("")
            self._change_button_display_on_getting(ConnectState.TO_WAITING)

    #--------------------------------------------------
    #時刻設定ボタン押下処理
    async def set_time_button_execute(self):
        if self._selected_peripheral_entity is None:
            self._message_service.show_error("接続対象が選択されていません","対象不定")
            return

        result = self._message_service.show_question("PCと時刻を同期しますか？","同期確認")
        if result == QMessageBox.StandardButton.Ok:
            try:
                self._change_button_display_on_set_time(True)

                # 現在時刻の取得
                current_time:datetime = datetime.datetime.now()
                print(current_time)
                entity:CurrentTimeEntity = CurrentTimeEntity(current_time)

                await self._unit_of_work.current_time_entities_repository.send_current_time(
                    self._selected_peripheral_entity.mac_address,
                    entity
                    )
                self._message_service.show_information("時刻同期に成功しました","同期成功")
            except Exception as e:
                print(f"Error occured : {e}")
                self._message_service.show_error("時刻同期に失敗しました","同期失敗")
            finally:
                self._change_button_display_on_set_time(False)

    #--------------------------------------------------
    #logfileリスト取得ボタン押下処理
    async def get_log_file_list_button_execute(self):
        if self._selected_peripheral_entity is None:
            self._message_service.show_error("接続対象が選択されていません","対象不定")
            return

        try:
            self._change_button_display_on_log_file_list(True)

            #周辺機器を検索
            files:list[LogFileEntity] = await self._unit_of_work.log_file_entities_repository.get_log_file_list(self._selected_peripheral_entity.mac_address)

            #リストをクリア
            self._log_file_list_model.clear()

            #機器が見つからなければ終了
            if files is None:
                print("データが取得できませんでした")
                self._message_service.show_error("データが取得できませんでした","データ取得エラー")
                return

            #リストに取得機器名を登録
            for file in files:
                self._log_file_list_model.add_item(file)

        except Exception as e:
            print(f"Error occured in get_log_file_list_button_execute : {e}")
        finally:
            self._change_button_display_on_log_file_list(False)

    #--------------------------------------------------
    #logfileリスト選択変更時
    def log_file_list_view_selectionChanged(self,selected:QItemSelection,deselected:QItemSelection):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            self._selected_log_file_entity = self._log_file_list_model.get(index)
            print(f"{self._selected_log_file_entity.file_name}")

    #--------------------------------------------------
    #ログファイル取得ボタン押下処理
    async def get_log_file_button_execute(self):
        if self._selected_peripheral_entity is None:
            self._message_service.show_error("接続対象が選択されていません","対象不定")
            return
        print(self._save_path)
        if not os.path.exists(self._save_path):
            self._message_service.show_error("有効なパスを指定してください","パスエラー")
            return

        save_file_name = self._selected_peripheral_entity.device_name + "_"  + self._selected_log_file_entity.file_name + ".csv"
        print(save_file_name)
        if os.path.isfile(f"{self._save_path}/{save_file_name}"):
            result = self._message_service.show_question("同名のファイルが存在します。上書きしますか？","上書き確認")
            if result == QMessageBox.StandardButton.Cancel:
                return

        try:
            self._change_button_display_on_get_log_file(True)

            # ログを取得
            logdata = await self._unit_of_work.log_file_entities_repository.get_log_file(self._selected_peripheral_entity.mac_address,self._selected_log_file_entity)

            # ログをファイルに保存
            with open(f"{self._save_path}/{save_file_name}","w") as f:
                for log in logdata:
                    f.write(f"{log}\n")

            self._message_service.show_information("ログの取得が完了しました","取得完了")

            self._change_button_display_on_get_log_file(False)

        except Exception as e:
            print(f"Error occured in get_log_file_button_execute : {e}")

    #--------------------------------------------------
    #ログファイル削除ボタン押下処理
    async def delete_log_file_button_execute(self):
        if self._selected_peripheral_entity is None:
            self._message_service.show_error("接続対象が選択されていません","対象不定")
            return

        if self._selected_log_file_entity is None:
            self._message_service.show_error("削除対象が選択されていません","対象不定")
            return

        result = self._message_service.show_question("一度削除すると元に戻せません。本当に削除しますか？","最終確認")
        if result == QMessageBox.StandardButton.Cancel:
            return

        try:
            self._change_button_display_on_delete_log_file(True)

            await self._unit_of_work.log_file_entities_repository.delete_log_file(self._selected_peripheral_entity.mac_address,self._selected_log_file_entity)
            self._log_file_list_model.remove_item(self._selected_log_file_entity)

            self._message_service.show_information("ログの削除が完了しました","削除完了")

            self._change_button_display_on_delete_log_file(False)
        except Exception as e:
            print(f"Error occured in delte_log_file_button_execute : {e}")

    #--------------------------------------------------
    #フォルダテキストボックス変更時処理
    def output_folder_qLineEdit_texeChanged(self,text:str):
        print(text)
        self._save_path=text

    #--------------------------------------------------
    #フォルダ選択ボタン押下処理
    def folder_select_button_execute(self):
        file_path = QFileDialog.getExistingDirectory()
        self._save_path = file_path
        self.output_folder_qLineEdit_text.emit(file_path)

    #--------------------------------------------------
    #終了ボタン押下処理
    def exit_button_execute(self):
        result  = self._message_service.show_question("ウィンドウを閉じてもよろしいですか？","終了確認")
        if result == QMessageBox.StandardButton.Ok:
            self.request_exit.emit()