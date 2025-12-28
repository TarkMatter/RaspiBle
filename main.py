import asyncio

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop  # PySide6 用の asyncio イベントループ
import sys

import Form.Views.mainWindow as MW
from Form.ViewModels.mainWindowViewModel import MainWindowViewModel
from Infrastructure.Bleak.unit_of_work_bleak import UnitOfWorkBleak
from Domain.Helper.message_service import MessageService

def main():
    #ainWindowのviewModelの生成
    _mainWindowViewModel = MainWindowViewModel(UnitOfWorkBleak(),MessageService())
    app = QApplication(sys.argv) # PySide6の実行
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        window = MW.MainWindow(_mainWindowViewModel) # ユーザがコーディングしたクラス
        window.show() # PySide6のウィンドウを表示

        with loop:
            loop.run_forever()

    finally: # PySide6の終了
        loop.close()

main()