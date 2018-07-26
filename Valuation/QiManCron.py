# -*- coding: utf-8 -*-
import platform

import requests_html
from selenium import webdriver

from Valuation.models import QIMAN


class QiMan(object):
    def __init__(self):
        self.url = "https://qieman.com/idx-eval"
        self.attrs = ['.group-LOW', '.group-MID', '.group-HIGH', '.group-NA']
        self.list = []

    def get_page_source(self):
        sysstr = platform.system()
        if sysstr == "Windows":
            browser = webdriver.PhantomJS()
        else:
            browser = webdriver.PhantomJS(executable_path="/opt/model/phantomjs/bin/phantomjs")
        browser.get(self.url)
        dom = browser.page_source

        html = requests_html.HTML(html=dom)
        print('获取到了HTML')
        return html

    def analysis(self):
        html = self.get_page_source()
        date = html.find('.qm-header-note')[0].find('p')[0].text.split(" ")[0]
        for attr in self.attrs:
            for i in html.find(attr)[0].find('.flex-table-row'):
                list = i.text.split('\n')[1:]
                list.append(i.find('span')[0].text)
                list.append(i.find('span')[1].text)
                list.append(attr)
                self.list.append(list)
        print('解析完成')
        for i in self.list:
            i[0] = float(i[0])
            i[2] = float(i[2])
            i[3] = float(i[3])
            i[4] = float(i[4])
            if i[7] == ".group-LOW":
                color = 'LOW'
            elif i[7] == ".group-MID":
                color = "MID"
            elif i[7] == ".group-HIGH":
                color = "HIGH"
            else:
                color = "NA"
            if i[1] == "--":
                percentile = 0
            else:
                percentile = float(i[1])

            if i[7] == ".group-LOW":
                color = 'LOW'
            elif i[7] == ".group-MID":
                color = "MID"
            elif i[7] == ".group-HIGH":
                color = "HIGH"
            else:
                color = "NA"
            if i[1] == "--":
                percentile = 0
            else:
                percentile = float(i[1])

            QIMAN.objects.update_or_create(
                name=i[5], code=i[6], PE_PB=i[0], percentile=percentile, high=i[2], low=i[3],
                roe=i[4], color=color, date=date
            )
        print("存储完成")


def my_job():
    QiMan().analysis()
