import requests
import os
import psycopg2
import sys

from src.classes import Employee, DBManager


PASSWORD_POSTGRES = os.environ.get('PASSWORD_POSTGRES')
database_name = 'course_project_bd'


def employer(sphere_employer):
    """Функция, получающая 10 работодателей в определенной сфере"""
    url = (f'https://api.hh.ru/employers?text={sphere_employer}'
           f'&only_with_vacancies=true&sort_by=by_vacancies_open'
           f'&employer_type="company"')

    response = requests.get(url)
    return response.json()['items'][:10]


def create_database():
    """Создание базы данных и необходимых таблиц"""
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=PASSWORD_POSTGRES
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(
        host='localhost',
        database=database_name,
        user='postgres',
        password=PASSWORD_POSTGRES
    )

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers(
            employer_id smallint PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            company_url_HeadHunter VARCHAR NOT NULL,
            quantity_vacancies smallint NOT NULL,
            information TEXT)
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies(
            vacancy_id smallint PRIMARY KEY,
            vacancy_name VARCHAR(255) NOT NULL,
            salary_on_HeadHunter INTEGER,
            vacancy_url_HeadHunter VARCHAR(255),
            area VARCHAR(255),
            published_at DATE,
            employer_id smallint REFERENCES employers(employer_id))
        """)

    conn.commit()
    conn.close()


def save_data_to_database(global_world):
    """Сохранение всей информации о работодателях и вакансиях в базу данных"""
    conn = psycopg2.connect(
        host='localhost',
        database=database_name,
        user='postgres',
        password=PASSWORD_POSTGRES
    )
    conn.autocommit = True
    cur = conn.cursor()

    list_vac = []
    for ind, val in enumerate(employer(global_world)):
        emp = Employee(val)
        emp.top_vacancies()
        emp_save = emp.for_save_to_database()
        list_vac.append({'name_employer': emp.name, 'list_vacancies': emp.list_vacancies})

        cur.execute("INSERT INTO employers VALUES (%s, %s, %s, %s, %s)", (ind + 1,
                                                                          emp_save['name'],
                                                                          emp_save['url'],
                                                                          emp_save['quantity_vacancies'],
                                                                          emp_save['info']))

    score = 0
    for index, value in enumerate(list_vac):
        for vac in value['list_vacancies']:
            score += 1
            if type(vac['salary']) != int:
                vac['salary'] = None
            cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)", (int(score),
                                                                                      str(vac['name']),
                                                                                      vac['salary'],
                                                                                      str(vac['url']),
                                                                                      str(vac['area']),
                                                                                      vac['published_at'],
                                                                                      index + 1))
    cur.close()
    conn.close()


def is_stop(word):
    if word.upper() == "STOP":
        sys.exit()


def check(user_answer):
    is_stop(user_answer)
    try:
        user_ch = int(user_answer)
    except:
        return False
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
        return True
