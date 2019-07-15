# KUR-dev-machine
#map <F8> :wa<CR>:lcd /home/kur/dev/SickZil-Machine/src<CR>:!python main.py<CR>
#map <F5> :wa<CR>:lcd /home/kur/dev/SickZil-Machine/test<CR>:!pytest -vv<CR>
# KUR-LAB-MACHINE
#map <F8> :wa<CR>:lcd /home/kur/dev/szmc/SickZil-Machine/src<CR>:!python main.py<CR>
#map <F5> :wa<CR>:lcd /home/kur/dev/szmc/SickZil-Machine/test<CR>:!pytest -vv<CR>

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    main_window = gui.MainWindow(engine)
    
    sys.exit(app.exec_())
