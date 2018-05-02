import numpy as np
import matplotlib.pyplot as plt


def calc_mdd(list_pv, plot=False):
    """
    MDD(Maximum Draw-Down) 계산
    :param list_pv: 포트폴리오 가치 리스트
    :return:
    """
    arr_pv = np.array(list_pv)
    peak_lower = np.argmax(np.maximum.accumulate(arr_pv) - arr_pv)
    peak_upper = np.argmax(arr_pv[:peak_lower])

    if plot:
        plt.plot(arr_pv)
        plt.plot([peak_upper, peak_lower], [arr_pv[peak_upper], arr_pv[peak_lower]], '.', color='red')
        plt.show()

    return (arr_pv[peak_lower] - arr_pv[peak_upper]) / arr_pv[peak_upper]


def _test_mdd():
    n = 1000
    list_pv = np.random.randn(n).cumsum()
    print(calc_mdd(list_pv))


if __name__ == '__main__':
    _test_mdd()