import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView

from weather.forms import CityForm
from weather.models import City


class HomeView(View):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eceb7384331a95f03360191abd202389'

    def get(self, *args, **kwargs):
        cities = City.objects.all()[:3]
        form = CityForm()

        city_list = []
        for city in cities:

            res = requests.get(self.url.format(city.name.lower())).json()
            city_weather = {
                'city': city.name,
                'temperature': res['main']['temp'],
                'description': res['weather'][0]['description'],
                'icon': res['weather'][0]['icon']
            }
            city_list.append(city_weather)

        return render(self.request, 'weather/index.html', {'city_list': city_list, 'form': form})

    def post(self, *args, **kwargs):
        form = CityForm(self.request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            res = requests.get(self.url.format(cd['name'].lower())).json()
            if res.get('cod') == '404':
                messages.warning(self.request, f"{cd['name'].title()}: {res['message'].title()}")
                return redirect('home')
            form.save()
            messages.success(self.request, f"City {cd['name'].title()} has been saved")

            return redirect('home')


