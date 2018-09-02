import platform

import requests_html
from django.db.models import Min, Max
from django.shortcuts import render
from selenium import webdriver

from .models import QIMAN


# Create your views here.


def index(request):
    name = request.GET.get('name', '上证50')
    format_date = []
    sz50 = QIMAN.objects.filter(name=name)
    names = QIMAN.objects.values('name').distinct().order_by('name')
    PE_PB = sz50.values_list('PE_PB', flat=True)
    date = sz50.values_list('date', flat=True)
    low = sz50.values('low').annotate(Min('low'))[0]['low__min']
    print(low)

    high = sz50.values('high').annotate(Max('high'))[0]['high__max']
    print(high)
    color_list = sz50.values_list('color')
    color = []
    for i in color_list:
        if i[0] == "LOW":
            color.append("green")
        elif i[0] == "HIGH":
            color.append("red")
        elif i[0] == "MID":
            color.append("yellow")
        else:
            color.append("gray")
    for i in date:
        format_date.append(i.strftime('%Y-%m-%d'))
    context = {
        'name': names,
        'PE_PB': list(PE_PB),
        'date1': format_date,
        'high': high,
        'low': low,
        'color': color,
        'code': name
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
        sysstr = platform.system()
        if sysstr == "Windows":
            browser = webdriver.PhantomJS()
        else:
            browser = webdriver.PhantomJS(executable_path="/opt/model/phantomjs/bin/phantomjs")
        browser.get(self.url)
        dom = browser.page_source

        html = requests_html.HTML(html=dom)
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
