import requests
from django.shortcuts import render
import datetime as dt


def index(request):
    appid = '053c98c9c0a3368f0e8cd2db240f3c91'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&exclude=current&lang=ua&appid=' + appid
    city = 'Каланчак'
    res = requests.get(url.format(city)).json()

    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"],
        'current_time': dt.datetime.utcfromtimestamp(res['dt'] + res['timezone'])
    }

    context = {'info': city_info}

    return render(request, 'Main/index.html', context)
