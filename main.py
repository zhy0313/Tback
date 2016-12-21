# -*- coding: utf-8 -*-

"""
IPS
__author__ = ideaplat
__mtime__ = 2016/12/20
"""
import data.ready_data as get
import matplotlib.pyplot as plt
if __name__ == '__main__':

    getdata = get.Ready_Data()

    apple = getdata.Get_data("AAPL")
    # microsoft = getdata.Get_data("MSFT")
    # google = getdata.Get_data("GOOG")
    # facebook = getdata.Get_data("FB")
    # twitter = getdata.Get_data("TWTR")
    # netflix = getdata.Get_data("NFLX")

    stock = [("AAPL", apple),]

    order = getdata.Ma_Crossover_Orders(stock,3,5)

    # print order

    bk = getdata.BackTest(order, 10000, port_value=.5, batch=100, flat_commision=35)
    # print bk["Total Profit"]
    # bk["Total Profit"].groupby(level=0).apply(lambda x: x[-1]).plot()
    # plt.show()
