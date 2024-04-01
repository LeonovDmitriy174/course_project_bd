from src.functions import create_database, save_data_to_database
from src.classes import DBManager

# Чтобы создать базу данных, используйте команду ниже
create_database()
# Запрос пользовательского слова, для выбора сферы работодателя
user_world = input("Введите ключевую сферу, в которой будет проходить поиск работодателей[IT компания]: ")

if user_world in ['', ' ', 'yes', 'true', 't', 'y', 'yes', 'IT компания', 'IT']:
    user_world = 'IT компания'

# Для сохранения данных в базу данных
save_data_to_database(user_world)

# Для получения данных из базы данных используется класс DB Manager
for_example = DBManager()
for_example.get_companies_and_vacancies_count()
