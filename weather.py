from ProgramManager import *
from DatabaseUpdater import *


#
class WeatherConsole:

    def __init__(self):
        self.database = DatabaseManager()
        self.manager = MainManager()
        self.actions_available = ['Добавление прогнозов за диапазон дат в базу данных',
                                  'Получение прогнозов за диапазон дат из базы',
                                  'Создание открыток из полученных прогнозов',
                                  'Выведение полученных прогнозов на консоль']

    def __str__(self):
        return f'Выберите нужное действие из дальнейших:\n'

    def console_dispatcher(self):
        res = self.manager.past_data()
        print(res)
        print(self.__str__())
        for index, x in enumerate(self.actions_available, start=1):
            print(f'<{index}> {x}')
        choice = input('Введите номер действия: ')
        while not choice.isdigit():
            choice = input('Ввод некорректен, попробуйте ещё раз: ')
        else:
            if int(choice) <= len(self.actions_available):
                print('Введите даты в формате ГГГГ-ММ-ДД:')
                _from = input('Дату начала желаемого периода: ')
                _to = input('Дату конца желаемого периода: ')
                result = self.manager.action_processing(number_of_action=int(choice), date_from=_from, date_to=_to)
                print(result)
        yes_no = input('Хотите ли вы выполнить еще одно действие? да/нет ')
        if yes_no == 'да':
            self.console_dispatcher()
        else:
            print('До свидания')


if __name__ == '__main__':
    console = WeatherConsole()
    console.console_dispatcher()
