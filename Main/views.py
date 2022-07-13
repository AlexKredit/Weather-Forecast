import requests
from django.shortcuts import render
import datetime as dt
from Main.models import City


def first_search(request):
    return render(request, 'Main/first_search.html')


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


# def get_queryset(request):
#     query = request.GET.get('name')
#     object_list = City.objects.order_by('name').filter(name__icontains=query)
#     return object_list


def get_queryset(request):
    query = request.GET.get('name')
    return query


def index(request):
    base_url_current = 'http://api.openweathermap.org/data/2.5/weather?q='

    appid = '053c98c9c0a3368f0e8cd2db240f3c91'
    lang = "en"

    url_current = base_url_current + get_queryset(request) + '&units=metric&exclude=current' + '&lang=' + lang + '&appid=' + appid

    for city in get_queryset(request):
        res_current = requests.get(url_current.format(city)).json()
        lat = str(res_current['coord']['lat'])
        lon = str(res_current['coord']['lon'])
        base_url_forecast = 'https://api.openweathermap.org/data/2.5/onecall'
        url_forecast = base_url_forecast + '?lat=' + lat + '&lon=' + lon + '&units=metric&exclude=minutely,alerts' + '&lang=' + lang + '&appid=' + appid
        res_forecast = requests.get(url_forecast.format(city)).json()
        current_time = dt.datetime.utcfromtimestamp(res_current['dt'] + res_current['timezone'])
        current_time_str = current_time.strftime('%H:%M')
        current_date_str = current_time.strftime('%a, %b %d')
        sunrise_time = dt.datetime.utcfromtimestamp(res_current['sys']['sunrise'] + res_current['timezone'])
        sunrise_time_str = sunrise_time.strftime('%H:%M')
        sunset_time = dt.datetime.utcfromtimestamp(res_current['sys']['sunset'] + res_current['timezone'])
        sunset_time_str = sunset_time.strftime('%H:%M')
        city_info = {
            'city': get_queryset(request),
            'country': res_current['sys']['country'],
            'temp': toFixed(res_current["main"]["temp"]),
            'temp_feels_like': toFixed(res_current['main']['feels_like']),
            'temp_max': toFixed(res_current['main']['temp_max']),
            'temp_min': toFixed(res_current['main']['temp_min']),
            'wind_speed': toFixed(res_current['wind']['speed'], 1),
            'weatherType': res_current["weather"][0]["main"],
            'weatherTypeFull': res_current["weather"][0]["description"],
            'humidity': res_current["main"]["humidity"],
            'pressure': res_current["main"]["pressure"],
            'icon': res_current["weather"][0]["icon"],
            'current_time': current_time_str,
            'current_date': current_date_str,
            'sunrise_time': sunrise_time_str,
            'sunset_time': sunset_time_str,
            'cloudiness': res_current['clouds']['all']
        }
        tempMax_forecast = []
        tempMin_forecast = []
        day_forecast = []
        icon_forecast = []
        weather_forecast = []
        temp_h = []
        time_h = []
        for n in range(25):
            temp_h.append(res_forecast['hourly'][n]['temp'])
            time_h.append(dt.datetime.utcfromtimestamp(res_forecast['hourly'][n]['dt'] + res_forecast['timezone_offset']))
        for i in range(6):
            tempMax_forecast.append(res_forecast['daily'][i]['temp']['max'])
            tempMin_forecast.append(res_forecast['daily'][i]['temp']['min'])
            day_forecast.append(dt.datetime.utcfromtimestamp(res_forecast['daily'][i]['dt'] + res_forecast['timezone_offset']))
            icon_forecast.append(res_forecast['daily'][i]['weather'][0]['icon'])
            weather_forecast.append(res_forecast['daily'][i]['weather'][0]['main'])
        city_forecast_info = {
            'temp_Max1': toFixed(tempMax_forecast[1]),
            'temp_Max2': toFixed(tempMax_forecast[2]),
            'temp_Max3': toFixed(tempMax_forecast[3]),
            'temp_Max4': toFixed(tempMax_forecast[4]),
            'temp_Max5': toFixed(tempMax_forecast[5]),
            'temp_Min1': toFixed(tempMin_forecast[1]),
            'temp_Min2': toFixed(tempMin_forecast[2]),
            'temp_Min3': toFixed(tempMin_forecast[3]),
            'temp_Min4': toFixed(tempMin_forecast[4]),
            'temp_Min5': toFixed(tempMin_forecast[5]),
            'day1': day_forecast[1].strftime('%b, %a %d'),
            'day2': day_forecast[2].strftime('%b, %a %d'),
            'day3': day_forecast[3].strftime('%b, %a %d'),
            'day4': day_forecast[4].strftime('%b, %a %d'),
            'day5': day_forecast[5].strftime('%b, %a %d'),
            'icon1': icon_forecast[1],
            'icon2': icon_forecast[2],
            'icon3': icon_forecast[3],
            'icon4': icon_forecast[4],
            'icon5': icon_forecast[5],
            'weather1': weather_forecast[1],
            'weather2': weather_forecast[2],
            'weather3': weather_forecast[3],
            'weather4': weather_forecast[4],
            'weather5': weather_forecast[5],
            'temp_h1': toFixed(temp_h[1]),
            'temp_h2': toFixed(temp_h[4]),
            'temp_h3': toFixed(temp_h[7]),
            'temp_h4': toFixed(temp_h[10]),
            'temp_h5': toFixed(temp_h[13]),
            'temp_h6': toFixed(temp_h[16]),
            'temp_h7': toFixed(temp_h[19]),
            'temp_h8': toFixed(temp_h[22]),
            'time_h1': time_h[1].strftime('%H:%M'),
            'time_h2': time_h[4].strftime('%H:%M'),
            'time_h3': time_h[7].strftime('%H:%M'),
            'time_h4': time_h[10].strftime('%H:%M'),
            'time_h5': time_h[13].strftime('%H:%M'),
            'time_h6': time_h[16].strftime('%H:%M'),
            'time_h7': time_h[19].strftime('%H:%M'),
            'time_h8': time_h[22].strftime('%H:%M'),
        }
        context = {'info': city_info, 'info_forecast': city_forecast_info}
        return render(request, 'Main/index.html', context)
