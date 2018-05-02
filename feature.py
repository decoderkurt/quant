import sys
import time

from PyQt5.QtWidgets import QApplication
import pandas as pd

import kiwoom


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hts = kiwoom.Kiwoom()

    for _ in range(5):
        if not hts.kiwoom_GetConnectState():
            hts.kiwoom_CommConnect()
            time.sleep(5)
        else:
            break

    df = pd.read_csv('data/kospi_20180420.csv', header=0, converters={'종목코드': lambda x: str(x)})

    dict_datalist = {}

    def add_data(data):
        for k, v in data.items():
            if k not in dict_datalist:
                dict_datalist[k] = []
            dict_datalist[k].append(v)

    hts.dict_callback['주식기본정보'] = add_data
    for idx, row in df.iterrows():
        code = row['종목코드']
        hts.kiwoom_TR_OPT10001_주식기본정보요청(code)

