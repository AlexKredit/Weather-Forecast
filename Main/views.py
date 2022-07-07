import requests
from django.shortcuts import render
import datetime as dt
from Main.models import City


def first_search(request):
    return render(request, 'Main/first_search.html')


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def get_queryset(request):
    query = request.GET.get('name')
    object_list = City.objects.order_by('name').filter(name__icontains=query)
    return object_list


def index(request):
    base_url_current = 'http://api.openweathermap.org/data/2.5/weather?q='
    base_url_forecast = 'https://api.openweathermap.org/data/2.5/forecast?q='
    appid = '053c98c9c0a3368f0e8cd2db240f3c91'
    lang = "en"

    url_current = base_url_current + '{}&units=metric&exclude=current' + '&lang=' + lang + '&appid=' + appid
    url_forecast = base_url_forecast + '{}&units=metric&exclude=hourly&cnt=8' + \
                   '&lang=' + lang + '&appid=' + appid

    for city in get_queryset(request):
        res_current = requests.get(url_current.format(city)).json()
        res_forecast = requests.get(url_forecast.format(city)).json()
        current_time = dt.datetime.utcfromtimestamp(res_current['dt'] + res_current['timezone'])
        current_time_str = current_time.strftime('%H:%M')
        current_date_str = current_time.strftime('%a, %b %d')
        sunrise_time = dt.datetime.utcfromtimestamp(res_current['sys']['sunrise'] + res_current['timezone'])
        sunrise_time_str = sunrise_time.strftime('%H:%M')
        sunset_time = dt.datetime.utcfromtimestamp(res_current['sys']['sunset'] + res_current['timezone'])
        sunset_time_str = sunset_time.strftime('%H:%M')
        city_info = {
            'city': city,
            'country': res_current['sys']['country'],
            'temp': toFixed(res_current["main"]["temp"]),
            'temp_feels_like': toFixed(res_current['main']['feels_like']),
            'wind_speed': toFixed(res_current['wind']['speed'], 1),
            'weatherType': res_current["weather"][0]["main"],
            'weatherTypeFull': res_current["weather"][0]["description"],
            'humidity': res_current["main"]["humidity"],
            'pressure': res_current["main"]["pressure"],
            'icon': res_current["weather"][0]["icon"],
            'current_time': current_time_str,
            'current_date': current_date_str,
            'sunrise_time': sunrise_time_str,
            'sunset_time': sunset_time_str
        }
        A = []

        for i in res_forecast['list']:
            A += toFixed(i['main']['temp'])
        city_forecast_info = {
            'temp': toFixed(res_forecast["list"][0]["main"]["temp"]),
             'wind_forecast': A
        }
        context = {'info': city_info, 'info_forecast': city_forecast_info}
        return render(request, 'Main/index.html', context)
