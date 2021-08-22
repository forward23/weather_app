import datetime
import requests

from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from weather.forms import CityForm
from weather.models import City


class HomeView(View):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    def get(self, request, *args, **kwargs):
        cities = City.objects.all()[:3]
        form = CityForm()

        city_list = []
        for city in cities:
            res = requests.get(self.url.format(city.name.lower(), settings.OPEN_WEATHER_TOKEN)).json()
            city_weather = {
                'city': city.name,
                'temperature': res['main']['temp'],
                'description': res['weather'][0]['description'],
                'icon': res['weather'][0]['icon']
            }
            city_list.append(city_weather)

        return render(request, 'weather/index.html', {'city_list': city_list, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CityForm(self.request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            added_city = cd['name'].lower()

            # check if city is already exists in database
            if added_city in [city.name for city in City.objects.all()]:
                city = City.objects.get(name=added_city)
                city.added_at = timezone.now()
                city.save()
                return redirect('home')

            # check if city doesn't exists in OpenWeather
            res = requests.get(self.url.format(added_city, settings.OPEN_WEATHER_TOKEN)).json()
            if res.get('cod') == '404':
                messages.warning(request, f"{added_city.title()}: {res['message'].title()}")
                return redirect('home')

            city = City.objects.create(name=added_city)
            city.save()
            messages.success(request, f"City {added_city.title()} has been saved")

            return redirect('home')


class ForecastView(View):

    def get(self, request, *args, **kwargs):
        city = get_object_or_404(City, name=self.kwargs['city'])

        url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}'
        res = requests.get(url.format(city.name.lower(), settings.OPEN_WEATHER_TOKEN)).json()

        labels = [datetime.datetime.utcfromtimestamp(i['dt']).strftime('%Y-%m-%d %H:%M') for i in res['list']]
        temperatures = {
            'temperature': [i['main']['temp'] for i in res['list']],
            'feels_like': [i['main']['feels_like'] for i in res['list']],
        }
        metrics = {
            'humidity': [i['main']['humidity'] for i in res['list']],
            'wind': [i['wind']['speed'] for i in res['list']],
        }

        return render(request, 'weather/forecast.html',
                      {'temperatures': temperatures, 'metrics': metrics, 'labels': labels, 'city': city.name})
