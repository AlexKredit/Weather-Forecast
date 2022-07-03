import requests
from django.shortcuts import render
import datetime as dt


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def index(request):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    appid = '053c98c9c0a3368f0e8cd2db240f3c91'
    lang = "en"
    city = 'Odessa'
    url = base_url + city + '&units=metric&exclude=current' + '&lang=' + lang + '&appid=' + appid
    res = requests.get(url.format(city)).json()
    current_time = dt.datetime.utcfromtimestamp(res['dt'] + res['timezone'])
    current_time_str = current_time.strftime('%H:%M')
    current_date_str = current_time.strftime('%a, %b %d')
    sunrise_time = dt.datetime.utcfromtimestamp(res['sys']['sunrise'] + res['timezone'])
    sunrise_time_str = sunrise_time.strftime('%H:%M')
    sunset_time = dt.datetime.utcfromtimestamp(res['sys']['sunset'] + res['timezone'])
    sunset_time_str = sunset_time.strftime('%H:%M')
    city_info = {
        'city': city,
        'country': res['sys']['country'],
        'temp': toFixed(res["main"]["temp"]),
        'temp_feels_like': toFixed(res['main']['feels_like']),
        'wind_speed': toFixed(res['wind']['speed'], 1),
        'weatherType': res["weather"][0]["main"],
        'weatherTypeFull': res["weather"][0]["description"],
        'humidity': res["main"]["humidity"],
        'pressure': res["main"]["pressure"],
        'icon': res["weather"][0]["icon"],
        'current_time': current_time_str,
        'current_date': current_date_str,
        'sunrise_time': sunrise_time_str,
        'sunset_time': sunset_time_str
    }
    context = {'info': city_info}
    return render(request, 'Main/index.html', context)
