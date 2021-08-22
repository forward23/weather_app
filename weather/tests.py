from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.utils import timezone

from .forms import CityForm
from .models import City
from .views import HomeView, ForecastView


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'weather/index.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Add City')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Homepage')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)

    def test_homepage_get_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CityForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_homepage_post_form(self):
        City.objects.create(name='london', added_at=timezone.now())
        self.assertEqual(City.objects.all().count(), 1)
        self.assertEqual(City.objects.all()[0].name, 'london')


class ForecastPageTests(TestCase):
    def setUp(self):
        City.objects.create(name='london', added_at=timezone.now())
        url = reverse('forecast', args=('london',))
        self.response = self.client.get(url)

    def test_forecast_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_forecast_template(self):
        self.assertTemplateUsed(self.response, 'weather/forecast.html')

    def test_forecast_contains_correct_html(self):
        self.assertContains(self.response, 'forecast for 5 days')

    def test_forecast_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Forecastpage')

    def test_forecast_url_resolves_forecastview(self):
        view = resolve('/forecast/london/')
        self.assertEqual(view.func.__name__, ForecastView.as_view().__name__)
