import requests_html
from django.shortcuts import render
from selenium import webdriver

from .models import QIMAN

import datetime


# Create your views here.


def index(request):
    PE_PB = QIMAN.objects.filter(name="上证50").values_list('PE_PB', flat=True)
    date = QIMAN.objects.filter(name="上证50").values_list('date', flat=True)
    low = QIMAN.objects.filter(name='上证50').values('low').first()
    high = QIMAN.objects.filter(name='上证50').values('high').first()
    print(min)
    format_date = []
    for i in date:
        format_date.append(i.strftime('%Y-%m-%d'))
    context = {
        'PE_PB': list(PE_PB),
        'date1': format_date,
        'high': high,
        'low': low
    }
    return render(request, 'Valuation/index.html', context)


def scrapy_view(request):
    QiMan().analysis()
    return render(request, 'Valuation/index.html')


class QiMan(object):
    def __init__(self):
        self.url = "https://qieman.com/idx-eval"
        self.attrs = ['.group-LOW', '.group-MID', '.group-HIGH', '.group-NA']
        self.list = []

    def get_page_source(self):
        browser = webdriver.PhantomJS()
        browser.get(self.url)
        dom = browser.page_source

        html = requests_html.HTML(html=dom)
        return html

    def analysis(self):
        html = self.get_page_source()
        for attr in self.attrs:
            for i in html.find(attr)[0].find('.flex-table-row'):
                list = i.text.split('\n')[1:]
                list.append(i.find('span')[0].text)
                list.append(i.find('span')[1].text)
                list.append(attr)
                self.list.append(list)
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

            print(i)
            QIMAN.objects.update_or_create(
                name=i[5], code=i[6], PE_PB=i[0], percentile=percentile, high=i[2], low=i[3],
                roe=i[4],
                color=color
            )
