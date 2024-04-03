import sys

from src.functions import create_database, save_data_to_database
from src.classes import DBManager


print("Приветствую! Я помогу подобрать список работодателей и их вакансий угодной вам сфере деятельности")
print("Для выхода из программы введите STOP")
user_world = input("Введите сферу деятельности работодателя[IT компания - рекомендуется]: ").lower()

if user_word in ("", " ", "yes", "true", "it компания", "it", "y", "t"]
    user_word = "IT компания"

def is_stop(word):
    if world.upper() is "STOP":
        sys.exit()
        
is_stop(user_word)
        
create_database()
save_data_to_database(user_world)

while True:
    user_choice = (f"Выберите, что вы хоите получить.\n"
                   f"На текущий момент я могу предложить следующую информацию:\n"
                   f"1 - Список всех компаний и количество вакансий у каждой\n"
                   f"2 - Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на компанию"
                   f"3 - Среднюю зарплату по вакансиям"
                   f"4 - Список всех вакансий, у которых зарплата выше среднего"
                   f"5 - Список всех вакансий, в названии которых содержится переданное вами слово\n"
                   f"Для выхода из программы введите STOP").upper()
    is_stop(user_choice)
    try:
        user_ch = int(user_choise)
    except:
        user_choise = ("Пожалуйста, введите одно из предложенных чисел или STOP")
    else:
        data_from_bd = DBManager()
        if user_ch == 1:
            data_from_bd.get_companies_and_vacancies_count()
        elif user_ch == 2:
            data_from_bd.get_all_vacancies()
        elif user_ch == 3:
            print("Средняя зарплата составляет:")
            data_from_bd.get_avg_salary()
        elif user_ch == 4:
            data_from_bd.get_vacancies_with_higher_salary()
        elif user_ch == 5:
            keyword = input("Введите ключевое слово: ")
            data_from_bd.get_vacancies_with_keyword(keyword)
            