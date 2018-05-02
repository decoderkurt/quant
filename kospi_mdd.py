#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

import kiwoom


if __name__ == "__main__":
    # 에러 메시지 출력을 위한 훅
    def excepthook(type_, value, tback):
        print("%s %s %s" % (type_, value, tback), file=sys.stderr)
        sys.__excepthook__(type_, value, tback)
    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    obj_kiwoom = kiwoom.Kiwoom()
    res = obj_kiwoom.kiwoom_CommConnect()
    # obj_kiwoom.kiwoom_TR_OPT10081_주식일봉차트조회('035420', '20180408')

    sys.exit(app.exec_())
