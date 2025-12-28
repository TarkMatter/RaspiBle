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
        # self._vm.current_value.connect(self._current_value_changed)

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
        self._vm.current_value_text.connect(self._now_current_value_label.setText)
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

    #------------------------------
    #現在電流値のSignal通知取得
    # def _current_value_changed(self,entity:RealTimeDataEntity):
    #     self._now_current_value_label.setText(f"{entity.current:.2f}A")