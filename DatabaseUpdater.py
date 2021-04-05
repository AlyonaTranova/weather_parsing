import os
import peewee
import datetime
from playhouse.db_url import connect
from WeatherMaker import WeatherMaker

database_proxy = peewee.DatabaseProxy()
db = connect(os.environ.get('DATABASE') or 'sqlite:///weather.db')
database_proxy.initialize(db)


class BaseTable(peewee.Model):
    class Meta:
        database = database_proxy


class Weather(BaseTable):
    date = peewee.CharField()
    date_in_text = peewee.CharField()
    temperature = peewee.CharField()
    conditions = peewee.CharField()


database_proxy.create_tables([Weather])


class DatabaseManager:

    def __init__(self):
        self.weather_data = Weather(BaseTable)

    def add_data(self, data):
        data_to_save = data
        for data in data_to_save:
            weather, created = self.weather_data.get_or_create(date=str(data),
                                                               defaults={'date_in_text': data_to_save[data][0],
                                                                         'temperature': data_to_save[data][1],
                                                                         'conditions': data_to_save[data][2]}
                                                               )
            if not created:
                query = self.weather_data.update(date_in_text=data_to_save[data][0], temperature=data_to_save[data][1],
                                                 conditions=data_to_save[data][2]).where(Weather.id == weather.id)

                query.execute()

    def add_past_data(self, data_list):
        for days in data_list:
            Weather.create(date=days, date_in_text=data_list[days][0], temperature=data_list[days][1],
                           conditions=data_list[days][2])

    def show_data(self, date_from, date_to):
        list_of = {}
        for days in Weather.select().where(Weather.date.between(date_from, date_to)):
            if days not in list_of:
                list_of[days.date_in_text] = days.conditions, days.temperature
        return list_of
