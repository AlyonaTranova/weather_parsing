import datetime
import requests
from bs4 import BeautifulSoup


class WeatherMaker:

    def __init__(self):
        self.url = 'https://yandex.ru/pogoda/moscow'
        self.weather_dict = {}
        self.past_weather = {}

    def parsing(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            list_of_dates = html_doc.find_all('time', {'class': 'time forecast-briefly__date'})
            list_of_temp = html_doc.find_all('span', {'class': 'temp__value temp__value_with-unit'})
            list_of_weather = html_doc.find_all('div', {'class': 'forecast-briefly__condition'})

            return zip(list_of_dates, list_of_temp, list_of_weather)

    def weather_processing(self, _from, _to):
        weather_parsing = self.parsing()
        for dates, temp, weather in weather_parsing:
            date = dates.get('datetime')[:10]
            date_as_time = datetime.datetime.strptime(date, "%Y-%m-%d")
            from_ = datetime.datetime.strptime(_from, "%Y-%m-%d")
            to_ = datetime.datetime.strptime(_to, "%Y-%m-%d")
            if from_ <= date_as_time <= to_:
                if date_as_time not in self.weather_dict:
                    self.weather_dict[str(date_as_time)[:10]] = dates.text, temp.text, weather.text

        return self.weather_dict

    def load_past_data(self):
        weather_parsing = self.parsing()
        for dates, temp, weather in weather_parsing:
            date = dates.get('datetime')[:10]
            date_as_time = datetime.datetime.strptime(date, "%Y-%m-%d")
            today = datetime.datetime.today()
            if date_as_time < today:
                if date_as_time not in self.weather_dict:
                    self.past_weather[str(date_as_time)[:10]] = dates.text, temp.text, weather.text

        return self.past_weather
