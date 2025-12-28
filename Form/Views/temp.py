from PySide6.QtWidgets import  QApplication,QWidget,QGridLayout
from PySide6.QtWidgets import QLabel, QPushButton,QButtonGroup,QRadioButton,QCheckBox
from PySide6.QtWidgets import QLineEdit, QTextEdit,QListView
from PySide6.QtCore import Qt     # Qtの状態変数の取得に必要（チェックボックスの入力状態の取得に使う）
from PySide6.QtCore import QObject
from PySide6.QtGui import QGuiApplication,QFont,QPixmap,QPalette,QColor

from Form.ViewModels.mainWindowViewModel import MainWindowViewModel
from Domain.Entities.realtime_data_entity import RealTimeDataEntity
import asyncio,time
#---------------------------------------------------
# PySide6のアプリ本体（ユーザがコーディングしていく部分）
class MainWindow(QWidget):
    def __init__(self, vm:QObject):
        super().__init__()
        self._vm:MainWindowViewModel = vm

        #現在電流値の変更取得登録
        self._vm.current_value.connect(self._current_value_changed)

        # ウィンドウタイトル
        self.setWindowTitle("BLE Test")
        palette = self.palette() # ウィンドウの色を取得
        palette.setColor(QPalette.Window, QColor("snow"))
        self.setPalette(palette) # ウィンドウの色を変更

        # 現在のスクリーンのジオメトリを取得
        screen_geometry = QGuiApplication.primaryScreen().geometry()

        # ウィンドウの位置とサイズを指定（px単位）
        windowWidth = 640   # ウィンドウの横幅
        windowHeight = 500  # ウィンドウの高さ
        xPos = (screen_geometry.width() - windowWidth) // 2 # x座標
        yPos = (screen_geometry.height() - windowHeight) // 2 # y座標

        # ウィンドウの位置とサイズの変更
        self.setGeometry(xPos, yPos, windowWidth, windowHeight)

        #閉じるボタンの無効化
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        layout: QGridLayout = QGridLayout() # グリッドレイアウトを使うことを宣言

        #高さ
        layout.setRowMinimumHeight(0, 50)
        layout.setRowMinimumHeight(1, 5)
        layout.setRowMinimumHeight(2, 50)
        layout.setRowMinimumHeight(3, 5)
        layout.setRowMinimumHeight(4, 50)
        layout.setRowMinimumHeight(5, 5)
        layout.setRowMinimumHeight(6, 50)
        layout.setRowMinimumHeight(7, 5)
        layout.setRowMinimumHeight(8, 50)
        layout.setRowMinimumHeight(9, 5)
        layout.setRowMinimumHeight(10, 50)
        layout.setRowMinimumHeight(11, 5)
        layout.setRowMinimumHeight(12, 50)
        layout.setRowMinimumHeight(13, 5)
        layout.setRowMinimumHeight(14, 50)
        layout.setRowMinimumHeight(15, 5)

        #幅
        layout.setColumnMinimumWidth(0, 170)
        layout.setColumnMinimumWidth(1, 10)
        layout.setColumnMinimumWidth(2, 170)
        layout.setColumnMinimumWidth(3, 5)
        layout.setColumnMinimumWidth(4, 100)
        layout.setColumnMinimumWidth(5, 5)
        layout.setColumnMinimumWidth(6, 100)
        layout.setColumnMinimumWidth(7, 5)
        layout.setColumnMinimumWidth(8, 150)
        layout.setColumnStretch(9, 1)  # 列7の幅を伸縮可能に設定

        font = QFont("MS UI Gothic",16) # フォントを指定

        self._vm.request_exit.connect(QApplication.quit)

        #------------------------------
        #プライベート変数
        self._peripheral_list_view:QListView = QListView()

        #------------------------------
        # 検索ボタン
        self._search_button = QPushButton("周辺検索")
        self._search_button.setFont(font) # フォントを指定
        self._search_button.setFixedSize(170, 50)   # ボタンのサイズを変更
        self._search_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
                color:gray;
            }
        """)
        #イベント登録
        #押下時
        self._search_button.pressed.connect(lambda : asyncio.create_task(self._vm.search_button_execute()))
        #データバインディング
        self._vm.search_button_text.connect(self._search_button.setText) #SetText
        self._vm.search_button_enable.connect(self._search_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._search_button, 0, 0)

        #------------------------------
        # データ取得ボタン
        self._get_data_button = QPushButton("現在値取得")
        self._get_data_button.setFont(font) # フォントを指定
        self._get_data_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._get_data_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
            color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._get_data_button.pressed.connect(lambda: self._vm.get_data_button_execute())
        #データバインディング
        self._vm.get_data_button_text.connect(self._get_data_button.setText) #SetText
        self._vm.get_data_button_enable.connect(self._get_data_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._get_data_button, 2, 8)

        #------------------------------
        #リストボックス(Peripheralリスト)
        self._peripheral_list_view = QListView()
        self._peripheral_list_view.setFont(font)
        self._peripheral_list_view.setModel(self._vm._peripheral_list_model)
        # イベント登録
        #選択変更時
        self._peripheral_list_view.selectionModel().selectionChanged.connect(self._vm.peripheral_list_view_selectionChanged)
        #データバインディング
        self._vm.peripheral_list_enable.connect(self._peripheral_list_view.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._peripheral_list_view,2,0,9,3)

        #------------------------------
        #対象Peripheral名表示ラベル
        self._target_label = QLabel(self)
        self._target_label.setFont(font)
        self._target_label.setText("")
        self._target_label.setAlignment(Qt.AlignCenter)
        self._target_label.setStyleSheet("""
            QLabel {
                color:            black;     /* 文字色 */
                background-color: lightgray; /* 背景色 */
            }
        """)
        #データバインディング
        self._vm.target_label_text.connect(self._target_label.setText) #SetText
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._target_label,0,4,1,5)

        #------------------------------
        #現在値名ラベル
        self._now_current_label = QLabel(self)
        self._now_current_label.setFont(font)
        self._now_current_label.setText("現在値")
        self._now_current_label.setAlignment(Qt.AlignCenter)
        self._now_current_label.setStyleSheet("""
            QLabel {
                color: black;  /* 文字色 */
            }
        """)
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._now_current_label,2,4,1,1)

        #------------------------------
        #現在電流値の表示ラベル
        self._now_current_value_label = QLabel(self)
        self._now_current_value_label.setFont(font)
        self._now_current_value_label.setText("")
        self._now_current_value_label.setAlignment(Qt.AlignCenter)
        self._now_current_value_label.setStyleSheet("""
            QLabel {
                color:            black;  /* 文字色 */
                background-color: lightgray;  /* 背景色 */
            }
        """)
        self._vm.current_Value_text.connect(self._now_current_value_label.setText)
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._now_current_value_label,2,6,1,1)

        #------------------------------
        #ログファイルリストラベル
        self._log_list_label = QLabel(self)
        self._log_list_label.setFont(font)
        self._log_list_label.setText("ログファイルリスト")
        self._log_list_label.setAlignment(Qt.AlignCenter)
        self._log_list_label.setStyleSheet("""
            QLabel {
                color: black;  /* 文字色 */
            }
        """)
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._log_list_label,4,4,1,5)

        #------------------------------
        # ログファイル:リスト取得ボタン
        self._get_log_file_list_button = QPushButton("リスト取得")
        self._get_log_file_list_button.setFont(font) # フォントを指定
        self._get_log_file_list_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._get_log_file_list_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
            color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._get_log_file_list_button.pressed.connect(lambda: asyncio.create_task(self._vm.get_log_file_list_button_execute()))
        #データバインディング
        self._vm.get_log_file_list_button_text.connect(self._get_log_file_list_button.setText) #SetText
        self._vm.get_log_file_list_button_enable.connect(self._get_log_file_list_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._get_log_file_list_button, 6, 8,1,1)

        #------------------------------
        # ログ取得ボタン
        self._get_log_file_button = QPushButton("ログ取得")
        self._get_log_file_button.setFont(font) # フォントを指定
        self._get_log_file_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._get_log_file_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
            color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._get_log_file_button.pressed.connect(lambda: asyncio.create_task(self._vm.get_log_file_button_execute()))
        #データバインディング
        self._vm.get_log_file_button_text.connect(self._get_log_file_button.setText) #SetText
        self._vm.get_log_file_button_enable.connect(self._get_log_file_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._get_log_file_button, 8, 8,1,1)

        #------------------------------
        # ログ削除ボタン
        self._delete_log_file_button = QPushButton("ログ削除")
        self._delete_log_file_button.setFont(font) # フォントを指定
        self._delete_log_file_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._delete_log_file_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
            color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._delete_log_file_button.pressed.connect(lambda: asyncio.create_task(self._vm.delete_log_file_button_execute()))
        #データバインディング
        self._vm.delete_log_file_button_text.connect(self._delete_log_file_button.setText) #SetText
        self._vm.delete_log_file_button_enable.connect(self._delete_log_file_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._delete_log_file_button, 10, 8,1,1)

        #------------------------------
        #リストボックス(logfileリスト)
        self._log_file_list_view = QListView()
        self._log_file_list_view.setFont(font)
        self._log_file_list_view.setModel(self._vm._log_file_list_model)
        # イベント登録
        #選択変更時
        self._log_file_list_view.selectionModel().selectionChanged.connect(self._vm.log_file_list_view_selectionChanged)
        #データバインディング
        self._vm.log_file_list_enable.connect(self._log_file_list_view.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._log_file_list_view,6,4,5,3)
        #------------------------------
        # 時刻設定ボタン
        self._set_time_button = QPushButton("現在時刻設定")
        self._set_time_button.setFont(font) # フォントを指定
        self._set_time_button.setFixedSize(170, 50)   # ボタンのサイズを変更
        self._set_time_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
            color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._set_time_button.pressed.connect(lambda: asyncio.create_task(self._vm.set_time_button_execute()))
        #データバインディング
        self._vm.set_time_button_text.connect(self._set_time_button.setText) #SetText
        self._vm.set_time_button_enable.connect(self._set_time_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        # layout.addWidget(self._set_time_button, 12, 0)
        layout.addWidget(self._set_time_button, 0, 2)

        #------------------------------
        # 終了ボタン
        self._exit_button = QPushButton("終了")
        self._exit_button.setFont(font) # フォントを指定
        self._exit_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._exit_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
                color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._exit_button.pressed.connect(lambda: self._vm.exit_button_execute())
        #データバインディング
        self._vm.exit_button_enable.connect(self._exit_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._exit_button, 14, 8)

        #------------------------------
        #出力フォルダラベル
        self.output_folder_label = QLabel(self)
        self.output_folder_label.setFont(font)
        self.output_folder_label.setText("ログ出力フォルダ")
        self.output_folder_label.setAlignment(Qt.AlignCenter)
        self.output_folder_label.setStyleSheet("""
            QLabel {
                color: black;  /* 文字色 */
            }
        """)
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self.output_folder_label,12,0,1,1)

        #------------------------------
        #出力フォルダテキストボックス
        self.output_folder_qLineEdit = QLineEdit(self)
        self.output_folder_qLineEdit.setFont(font)
        self.output_folder_qLineEdit.setFixedHeight(50)

        # イベント登録
        # テキスト変更時
        self.output_folder_qLineEdit.textChanged.connect(lambda :self._vm.output_folder_qLineEdit_texeChanged(self.output_folder_qLineEdit.text()))
        #データバインディング
        self._vm.output_folder_qLineEdit_text.connect(self.output_folder_qLineEdit.setText) #SetText
        self._vm.output_folder_qLineEdit_enable.connect(self.output_folder_qLineEdit.setEnabled) #SetEnable

        layout.addWidget(self.output_folder_qLineEdit,12,2,1,5)

        #------------------------------
        # フォルダ選択ボタン
        self._folder_select_button = QPushButton("フォルダ選択")
        self._folder_select_button.setFont(font) # フォントを指定
        self._folder_select_button.setFixedSize(150, 50)   # ボタンのサイズを変更
        self._folder_select_button.setStyleSheet("""
            QPushButton {
                padding: 5px;                   /* ボタンの内側の余白 */
                background-color: lightgray;    /* 通常時の背景色 */
                color: black;                   /* 通常時のテキスト色 */
                border-radius: 5px;             /* 角を丸くする */
            }
            QPushButton:hover {
                background-color: lightblue;    /* ホバー時の背景色 */
            }
            QPushButton:pressed {
                background-color: lightgreen;   /* クリック時の背景色 */
            }
            QPushButton:disabled{
                color:gray;
            }
        """)
        # イベント登録
        #押下時
        self._folder_select_button.pressed.connect(lambda: self._vm.folder_select_button_execute())
        #データバインディング
        self._vm.folder_select_button_text.connect(self._folder_select_button.setText) #SetText
        self._vm.folder_select_button_enable.connect(self._folder_select_button.setEnabled) #SetEnabled
        # グリッドレイアウトにボタンを追加
        layout.addWidget(self._folder_select_button, 12, 8)

        #------------------------------
        #グリッドレイアウトをウィンドウに設定
        self.setLayout(layout)

    #--------------------------------------------------
    # async def _start_realtime_data_loop(self):
    #     realtime_data: RealTimeDataEntity | None = None
    #     while self._getting_data:
    #         try:
    #             realtime_data = await self._vm.get_realtime_data(
    #                 self._selected_peripheral_entity.mac_address
    #             )

    #             #データが取得できなければ終了
    #             if realtime_data is None:
    #                 print("データを取得できませんでした")
    #                 self._message_service.show_error("データを取得できませんでした","取得エラー")
    #                 self.change_button_isEnabled_on_get_data(True)
    #                 break

    #             print(realtime_data)
    #             timestr = time.strftime('%Y/%m/%d %H:%M:%S', realtime_data.now)
    #             print(f"{timestr} / {realtime_data.current}")

    #         except UnboundLocalError as e:
    #             print(f"error is : {e}")
    #         except asyncio.CancelledError:
    #             print("リアルタイムデータ取得タスクがキャンセルされました")
    #             self._message_service.show_information("キャンセルされました","キャンセル")
    #         except Exception as e:
    #             print(f"エラー j: {type(e)}")
    #             # self.ShowErrorMessage("エラー", f"{e}")
    #             # self._message_service.show_error(f"{e}")
    #             # raise Exception(e)
    #             # self._getting_data = False
    #             self.change_button_isEnabled_on_get_data(True)
    #             break  # エラーでループ停止

    #         await asyncio.sleep(1)  # 1秒待機

    #------------------------------
    #現在電流値のSignal通知取得
    def _current_value_changed(self,entity:RealTimeDataEntity):
        self._now_current_value_label.setText(f"{entity.current:.2f}A")


    # #------------------------------
    # #現在値取得ボタンの作成
    #     #--------------------
    #     #ボタン押下時の処理
    #     def CallGet_data_buttonPressed(self):
    #         if self._selected_peripheral_entity is None:
    #             # self.ShowMessageBox("対象不定","接続対象が選択されていません")
    #             self._message_service.show_error("接続対象が選択されていません","対象不定")
    #             return

    #         try:
    #             if not self._getting_data:
    #                 print("Getting start ...")
    #                 # self._getting_data = True
    #                 self.change_button_isEnabled_on_get_data(False)

    #                 if self._getdata_task is not None and not self._getdata_task.done():
    #                     self._getdata_task.cancel()

    #                 self._getdata_task = asyncio.create_task(self._start_realtime_data_loop())
    #             else:
    #                 print("Getting finish !")
    #                 # self._getting_data = False
    #                 self.change_button_isEnabled_on_get_data(True)
    #                 if self._getdata_task:
    #                     self._getdata_task.cancel()
    #         except UnboundLocalError as e:
    #             print(f"UnboundLocalError in CallGet_data_buttonPressed method : {e}")
    #         except Exception as e:
    #             print(f"Exception in CallGet_data_buttonPressed method : {e}")
    #         # finally:
    #         #     self._getting_data = False
    #         #     self.change_button_isEnabled_on_get_data(True)

    
    #         # async def fetch_entities():
    #         #     try:
    #         #         realtime_data:RealTimeDataEntity = await self._vm.get_realtime_data(self._selected_peripheral_entity.mac_address)
    #         #         # entities:list[PeripheralEntity] = await self._vm.get_device_all_entities()
    #         #         # self.add_device_list(entities)
    #         #         timestr = time.strftime('%Y/%m/%d %H:%M:%S',realtime_data.now)
    #         #         print(f"{timestr} / {realtime_data.current}")
    #         #     except Exception as e:
    #         #         print(f"エラー: {type(e)}")
    #         #         self.ShowErrorMessage("エラー",f"{e}")
    #         #     finally:
    #         #         self.change_button_isEnabled_on_get_data(True)

    #         # self.change_button_isEnabled_on_get_data(False)

    #         # asyncio.create_task(fetch_entities())
    #     #--------------------
    #     return btn

    # #----------
    # #検索中表示変更
    # def change_button_isEnabled_on_search(self,display:bool):
    #     self._search_button.setEnabled(display)
    #     self._get_data_button.setEnabled(display)
    #     self._exit_button.setEnabled(display)

    #     if display:
    #         self._search_button.setText("周辺検索")
    #     else:
    #         self._search_button.setText("検索中......")

    # #----------
    # #データ取得中表示変更
    # def change_button_isEnabled_on_get_data(self,display:bool):
    #     self._getting_data = not display
    #     self._search_button.setEnabled(display)
    #     # self._get_data_button.setEnabled(display)
    #     self._exit_button.setEnabled(display)

    #     if display:
    #         self._get_data_button.setText("データ取得")
    #     else:
    #         self._get_data_button.setText("取得中......")

    #------------------------------
    #取得したデバイス一覧をリストに追加
    # def add_device_list(self,entities:list[PeripheralEntity]):
    #     self._model.clear()
    #     self._model.addEntities(entities)

    #--------------------------------------------------
    #--------------------------------------------------
    #--------------------------------------------------
    #--------------------------------------------------
    #--------------------------------------------------
    def SetLabel(self):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）
        label = QLabel(self)

        # ラベルの見た目をQt Style Sheetで設定
        labelStyle = """QLabel {
            color:            #FF00AA;  /* 文字色 */
            font-size:        64px;     /* 文字サイズ */
            background-color: #FFAA00;  /* 背景色 */
        }"""

        # 見た目の設定をラベルに反映させる
        label.setStyleSheet(labelStyle)

        # ラベルに文字を指定
        label.setText("ラベル")

    #--------------------------------------------------
    def SetImage(self):
        # ラベルを使うことを宣言
        label = QLabel(self)

        # 画像の読み込み
        image = QPixmap(r".\xxx\xxx.png")

        # 画像サイズの変更
        width = image.size().width() / 2    # 横幅を半分に
        height = image.size().height() / 2  # 高さを半分に
        image = image.scaled(width, height) # 読み込んだ画像のサイズを変更

        # ラベルに画像を指定
        label.setPixmap(image)

    #--------------------------------------------------
    def SetButton(self):
        # ボタンを使うことを宣言
        button = QPushButton(self)

        # ボタンに表示する文字
        button.setText("押してみよう！！")

        # ボタンを押したら実行させる処理
        # connectメソッド: 処理させるメソッド
        button.pressed.connect(self.CallbackButtonPressed)

        # ボタンを離したら実行させる処理（引数を指定する場合）
        # connectメソッド: 処理させるメソッド
        button.released.connect(lambda: self.CallbackButtonReleased("離した"))

    # ボタンが押されたら実行させるメソッド
    # connectメソッドから呼び出される
    def CallbackButtonPressed(self):
        print("押したよ")

    # ボタンが離されたら実行させるメソッド（引数あり）
    # connectメソッドから呼び出される
    def CallbackButtonReleased(self, radian):
        print("今！　" + str(radian) + "よ！")

    #--------------------------------------------------
    # ラジオボタンは別のメソッドに分けました
    def SetRadio(self):
        # ボタン系ウィジェットをグループ化する
        self.radioGroup = QButtonGroup(self)

        # １つ目のラジオボタン
        self.radio1Id = 1                       # １つ目のラジオボタンID
        radio1 = QRadioButton(self)             # ラジオボタンを使うことを宣言
        radio1.setText("のどがからっから")      # ラジオボタンに表示する文字
        radio1.move(10, 10)                     # ラジオボタンの表示位置を絶対座標で指定
        self.radioGroup.addButton(radio1, self.radio1Id)    # グループに登録

        # ２つ目のラジオボタン
        self.radio2Id = 2                       # ２つ目のラジオボタンのID
        radio2 = QRadioButton(self)             # ラジオボタンを使うことを宣言
        radio2.setText("おぉいしぃ")            # ラジオボタンに表示する文字
        radio2.move(10, 35)                     # ラジオボタンの表示位置を絶対座標で指定
        self.radioGroup.addButton(radio2, self.radio2Id)    # グループに登録

        # ３つ目のラジオボタン
        self.radio3Id = 3                       # ３つ目のラジオボタンID
        radio3 = QRadioButton(self)             # ラジオボタンを使うことを宣言
        radio3.setText("ス●ンジ・ボブだよ")    # ラジオボタンに表示する文字
        radio3.move(10, 60)                     # ラジオボタンの表示位置を絶対座標で指定
        self.radioGroup.addButton(radio3, self.radio3Id)    # グループに登録

        # １つ目のラジオボタンを初期入力状態にする
        radio1.setChecked(True)

        # いずれかのラジオボタンがクリックされたら実行させる処理
        self.radioGroup.buttonClicked.connect(self.CallbackRadioStatechanged)

    # ラジオボタンをクリックされたら実行されるメソッド
    def CallbackRadioStatechanged(self):
        # １つ目のラジオボタンを選択したとき（checkedIdメソッドで選択中のボタンIDを取得）
        if self.radioGroup.checkedId() == self.radio1Id:
            print("1")
            # self.commentImage = QPixmap(r".\img\radio_001.png") # ふきだし画像読み込み
            commentXPos = 200   # ふきだし画像の表示x座標
            commentYPos = 600   # ふきだし画像の表示y座標
        # ２つ目のラジオボタンを選択したとき（checkedIdメソッドで選択中のボタンIDを取得）
        elif self.radioGroup.checkedId() == self.radio2Id:
            print("2")
            # self.commentImage = QPixmap(r".\img\radio_002.png") # ふきだし画像読み込み
            commentXPos = 0     # ふきだし画像の表示x座標
            commentYPos = 500   # ふきだし画像の表示y座標
        # ３つ目のラジオボタンを選択したとき（checkedIdメソッドで選択中のボタンIDを取得）
        elif self.radioGroup.checkedId() == self.radio3Id:
            print("3")
            # self.commentImage = QPixmap(r".\img\radio_003.png") # ふきだし画像読み込み
            commentXPos = 600   # ふきだし画像の表示x座標
            commentYPos = 100   # ふきだし画像の表示y座標

    #--------------------------------------------------
    def SetCheckbox(self):
        # 今回はリスト（配列）を使ってみましょう
        self.chBox = []

        # １つ目のチェックボックス
        self.chBox.append(QCheckBox(self))  # チェックボックスを追加
        self.chBox[0].move(10, 10)          # チェックボックスの表示位置を絶対座標で指定
        self.chBox[0].setText("赤")         # チェックボックスに表示する文字
        self.chBox[0].setStyleSheet("background-color: white")  # チェックボックスの背景色を白にする
        # １つ目のチェックボックスの入力状態が変化したら呼び出す処理
        self.chBox[0].stateChanged.connect(self.CallbackCheckboxStatechanged)

        # ２つ目のチェックボックス
        self.chBox.append(QCheckBox(self))  # チェックボックスを追加
        self.chBox[1].move(10, 35)          # チェックボックスの表示位置を絶対座標で指定
        self.chBox[1].setText("緑")         # チェックボックスに表示する文字
        self.chBox[1].setStyleSheet("background-color: white")  # チェックボックスの背景色を白にする
        # ２つ目のチェックボックスの入力状態が変化したら呼び出す処理
        self.chBox[1].stateChanged.connect(self.CallbackCheckboxStatechanged)

        # ３つ目のチェックボックス
        self.chBox.append(QCheckBox(self))  # ３つ目のチェックボックスを追加
        self.chBox[2].move(10, 60)          # チェックボックスの表示位置を絶対座標で指定
        self.chBox[2].setText("青")         # チェックボックスに表示する文字
        self.chBox[2].setStyleSheet("background-color: white")  # チェックボックスの背景色を白にする
        # ３つ目のチェックボックスの入力状態が変化したら呼び出す処理
        self.chBox[2].stateChanged.connect(self.CallbackCheckboxStatechanged)

    # チェックボックスの入力状態が変化したら実行する処理
    def CallbackCheckboxStatechanged(self):
        # 三原色（16進数）
        red   = 0x00
        green = 0x00
        blue  = 0x00

        if self.chBox[0].checkState() == Qt.Checked:
            red |= 0xAA     # ちょっと暗めの赤
        else:
            red |= 0x00     # 赤要素を無くす

        if self.chBox[1].checkState() == Qt.Checked:
            green |= 0xAA   # ちょっと暗めの緑
        else:
            green |= 0x00   # 緑要素を無くす

        if self.chBox[2].checkState() == Qt.Checked:
            blue |= 0xAA    # ちょっと暗めの青
        else:
            blue |= 0x00    # 青要素を無くす

        # RGBカラーコードに変換
        color = "#{0:02x}{1:02x}{2:02x}".format(red, green, blue)

        # 背景色を変更
        self.setStyleSheet("background-color: " + color + ";")

    #--------------------------------------------------
    def SetLineEdit(self):
        self.lineEdit = QLineEdit(self) # 入力欄を使うことを宣言
        self.lineEdit.move(0, 25)       # 入力欄の表示位置を絶対座標で指定
        self.lineEdit.resize(200, 25)   # 入力欄のサイズを変更

        # 入力欄でEnterキーが押されたら実行する処理を呼び出す
        self.lineEdit.returnPressed.connect(self.CallbaclReturnpressedLineedit)

    # 入力欄でEnterキーが押されたら実行する処理
    def CallbaclReturnpressedLineedit(self):
        # 入力された内容を表示（text()メソッドで入力内容を取り出している）
        print(self.lineEdit.text())

    #--------------------------------------------------
    def SetTextEdit(self):
        self.textEdit = QTextEdit(self) # テキストボックスを使うことを宣言
        self.textEdit.move(0, 25)       # テキストボックスの表示位置を絶対座標で指定

        # ウィンドウのサイズを取得
        windowWidht = self.size().width()   # ウィンドウの横幅
        windowHeight = self.size().height() # ウィンドウの高さ

        # テキストボックスのサイズをウィンドウサイズに合わせる
        self.textEdit.resize(windowWidht, windowHeight)

    # ボタンがクリックされたら実行する処理
    def CallbackClickedPushbutton(self):
        # テキストボックスに書かれている内容を表示するだけ
        print(self.textEdit.toPlainText())