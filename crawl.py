from ntpath import join
from bs4 import BeautifulSoup
import operator
from matplotlib.font_manager import json_dump
import requests
import json as _JSON
import html

list_of_year = [1401]  # 1402, 1403, 1404 You can add years
# Days of the month that are usually holiday. This means weekends
list_of_normal_holiday = [5, 6, 12, 13, 19, 20, 26, 27, 33, 34]

list_of_holiday_optimize = []
list_of_event_holiday = []

url = 'https://www.time.ir/'  # Target site

for year in list_of_year:
    print("crowling year: "+str(year))
    for month in range(1, 13):  # Range 1 to 12 per month in years, you can customize that
        print("crowling month: "+str(month) + " doing")

        list_of_event_holiday.clear()
        data = {}
        data['Year'] = year
        data['Month'] = month
        data['Base1'] = 0
        data['Base2'] = 1
        data['Base3'] = 2
        data['Responsive'] = True

        res = requests.get(url=url, params=data, data=data)

        dataRes = html.unescape(res.text)
        soup = BeautifulSoup(dataRes, 'html.parser')

        for li in soup.find_all('li', {'class': 'eventHoliday'}):
            clearText = li.get_text().replace('\n', '').replace('\r', '')
            cleanText = " ".join(clearText.split())
            arrayText = cleanText.split()

            res = {}
            res['year'] = data['Year']
            res['month'] = data['Month']
            res['day'] = int(arrayText[0])

            arrayText.pop(0)
            arrayText.pop(0)

            res['Title'] = " ".join(map(str, arrayText))

            list_of_event_holiday.append(res)

        if (len(list_of_event_holiday) > 0):
            jsonString = _JSON.dumps(list_of_event_holiday)
            jsonFile = open("list_of_event_holiday-" +
                            str(res['year'])+"-"+str(res['month'])+".json", "w")
            jsonFile.write(jsonString.encode("utf-8").decode('unicode-escape'))
            jsonFile.close()

        for objs in soup.findAll('div', class_='dayList'):
            divs = objs.findChildren("div", {'style': 'width:14.28%'})
            for index, div in enumerate(divs):
                if not operator.contains(str(div), "spacer disabled"):
                    rsData = {}
                    rsData['year'] = year
                    rsData['month'] = month

                    day = div.findChildren("div", {"class": "jalali"})
                    rsData['day'] = int(day[0].text)

                    rsData['isHoliDay'] = False
                    rsData['title'] = None

                    if operator.contains(str(div), "holiday"):
                        for item in list_of_event_holiday:
                            if (item['year'] == rsData['year'] and item['month'] == rsData['month'] and item['day'] == rsData['day']):
                                rsData['title'] = item['Title']
                        rsData['isHoliDay'] = True

                    if (index in list_of_normal_holiday):
                        rsData['title'] = 'تعطیلات آخر هفته'
                        rsData['isHoliDay'] = True

                    list_of_holiday_optimize.append(rsData)

        print("crowling "+str(year) + " - " + str(month) + " done")
        print('-' * 80)

jsonString = _JSON.dumps(list_of_holiday_optimize)
jsonFile = open("list_of_holiday_optimize.json", "w")
jsonFile.write(jsonString.encode("utf-8").decode('unicode-escape'))
jsonFile.close()
