import time
import win32com.client
import pandas as pd


# 로거 생성 및 로깅 포멧 설정
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')

# 로그 파일 핸들러
# fh_log = TimedRotatingFileHandler('logs/log', when='midnight', encoding='utf-8', backupCount=120)
# fh_log.setLevel(logging.DEBUG)
# fh_log.setFormatter(formatter)
# logger.addHandler(fh_log)

# 콘솔 핸들러
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)


class Creon:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    def creon_7400_주식차트조회(self, code, date_from, date_to):
        b_connected = self.obj_CpCybos.IsConnect
        if b_connected == 0:
            logger.info("연결 실패")
            return None

        list_field_key = [0, 1, 2, 3, 4, 5, 8]
        list_field_name = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        dict_chart = {name: [] for name in list_field_name}

        self.obj_StockChart.SetInputValue(0, 'A'+code)
        self.obj_StockChart.SetInputValue(1, ord('1'))  # 0: 개수, 1: 기간
        self.obj_StockChart.SetInputValue(2, date_to)  # 종료일
        self.obj_StockChart.SetInputValue(3, date_from)  # 시작일
        self.obj_StockChart.SetInputValue(5, list_field_key)  # 필드
        self.obj_StockChart.SetInputValue(6, ord('D'))  # 'D', 'W', 'M', 'm', 'T'
        self.obj_StockChart.BlockRequest()

        status = self.obj_StockChart.GetDibStatus()
        msg = self.obj_StockChart.GetDibMsg1()
        logger.info("통신상태: {} {}".format(status, msg))
        if status != 0:
            return None

        cnt = self.obj_StockChart.GetHeaderValue(3)  # 수신개수
        for i in range(cnt):
            dict_item = (
                {name: self.obj_StockChart.GetDataValue(pos, i) 
                for pos, name in zip(range(len(list_field_name)), list_field_name)}
            )
            for k, v in dict_item.items():
                dict_chart[k].append(v)

        logger.debug("차트: {} {}".format(cnt, dict_chart))
        return pd.DataFrame(dict_chart, columns=list_field_name)


if __name__ == '__main__':
    creon = Creon()
    print(creon.creon_7400_주식차트조회('035420', 20150101, 20171231))