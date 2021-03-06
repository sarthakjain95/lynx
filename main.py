'''
    main.py

    - Configures Global logger
    - Creates/shows UI and starts Qt application

    Note:
        - Add `"python.linting.pylintArgs": ["--extension-pkg-whitelist=PyQt5"]` to settings.json
            to disable import related warnings.
'''

import sys
import logging
import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from package import app


def main():
    ''' Creates UI and starts GUI event loop '''
    lynx = QApplication(sys.argv)
    # Load UI Font
    QtGui.QFontDatabase.addApplicationFont('./package/resources/fonts/Montserrat-Regular.ttf')
    # Start Application
    main_window = app.MainWindow()
    main_window.show()
    sys.exit(lynx.exec_())


if __name__ == "__main__":

    TIMESTAMP = str(int(time.time()))
    logfile = f"session-{TIMESTAMP}.log"
    # logfile = f"session.log"

    logging.basicConfig(
        format='''%(asctime)s [%(levelname)s] %(message)s''',
        datefmt="%H:%M:%S",
        filename=logfile,
        encoding="utf-8",
        level=logging.DEBUG
    )

    main()
