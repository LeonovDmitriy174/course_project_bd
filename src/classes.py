import requests
import re
import psycopg2
import os


PASSWORD_POSTGRES = os.environ.get('PASSWORD_POSTGRES')
database_name = 'course_project_bd'


class Employee:
    """Класс, для работы с работодателями"""
    def __init__(self, list_employer):
        self.id = list_employer['id']
        self.name = list_employer['name']
        self.url = list_employer['alternate_url']
        self.vacancies_url = list_employer['vacancies_url']
        self.__info = None
        self.quantity_vacancies = list_employer['open_vacancies']
        self.list_vacancies = None

    def __str__(self):
        return (f'Название:{self.name}\n'
                f'Url работодателя: {self.url}\n'
                f'Информация: {self.__info}\n'
                f'Количество вакансий: {self.quantity_vacancies}\n')

    @property
    def info(self):
        """Приведем информацию в более читаемый вид"""
        response = requests.get(f'https://api.hh.ru/employers/{self.id}')
        self.__info = response.json()['description']
        try:
            self.__info = (re.sub
                           ('<h2>|</h2>|</ol>|<ol>|nbsp;|</em>|<em>|</ul>|<ul>|<u>|</u>|</strong>|</p>|<p>|</li>|<li>|<strong>|&|quot;|<br />',
                            '', self.__info))
        except TypeError:
            pass
        finally:
            return self.__info

    def top_vacancies(self):
        """Работа с вакансиями работодателя"""
        response = requests.get(self.vacancies_url)
        list_vacancies = []
        for_print = []
        for vac in response.json()['items']:
            vacancy = Vacancy(vac)
            list_vacancies.append(vacancy.for_save_to_database())
            for_print.append(str(vacancy))
        self.list_vacancies = list_vacancies
        return for_print

    def for_save_to_database(self):
        """Метод, который подготавливает словарь для сохранения данных в базу данных"""
        employer = {'name': self.name,
                    'url': self.url,
                    'info': self.info,
                    'quantity_vacancies': self.quantity_vacancies}
        return employer


class Vacancy:
    """Класс, для работы с вакансиями"""
    id = None
    name = None
    url = None
    __salary = True
    area = None

    def __init__(self, vacancies):
        try:
            self.salary_from = vacancies['salary']['from']
            self.salary_to = vacancies['salary']['to']
        except TypeError:
            self.__salary = False
        else:
            if self.salary_from is None or self.salary_to is None:
                self.__salary = False
            else:
                self.salary_from = vacancies['salary']['from']
                self.salary_to = vacancies['salary']['to']
        finally:
            self.id = vacancies['id']
            self.name = vacancies['name']
            self.url = vacancies['alternate_url']
            self.area = vacancies['area']['name']
            self.date = vacancies['published_at']

    @property
    def salary(self):
        if self.__salary:
            return int((self.salary_to + self.salary_from) / 2)
        else:
            return 'Зарплата не указана'

    def __str__(self):
        return (f'\nНазвание: {self.name}\n'
                f'Зарплатная вилка: {self.salary}\n'
                f'Url вакансии: {self.url}\n'
                f'Место работы: {self.area}\n'
                f'Дата и время публиикации: {self.date[:10]} ({self.date[11:19]})\n')

    def for_save_to_database(self):
        """Метод, который подготавливает словарь для сохранения данных в базу данных"""
        vacancy = {'name': self.name,
                   'salary': self.salary,
                   'url': self.url,
                   'area': self.area,
                   'published_at': self.date}
        return vacancy


class DBManager:
    """Класс, для получения информации из базы данных"""
    def __init__(self, db_name=database_name):
        self.conn = psycopg2.connect(
            host='localhost',
            database=db_name,
            user='postgres',
            password=PASSWORD_POSTGRES
        )
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT company_name, quantity_vacancies FROM employers")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT company_name, vacancy_name, salary_on_headhunter, vacancy_url_headhunter
            FROM vacancies
            LEFT JOIN employers USING(employer_id)
            """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT AVG(salary_on_headhunter) FROM vacancies")
            row = cursor.fetchall()
            print(row[0][0])

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT vacancy_name, salary_on_headhunter
            FROM vacancies
            WHERE salary_on_headhunter > (SELECT AVG(salary_on_headhunter) FROM vacancies)
            """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, world_to_search):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT vacancy_name FROM vacancies")
            rows = cursor.fetchall()
            for row in rows:
                if world_to_search.lower() in row[0].lower():
                    print(row[0])
