from src.functions import create_database, save_data_to_database, check, is_stop

print("Приветствую! Я помогу подобрать список работодателей и их вакансий угодной вам сферы деятельности")
print("Для выхода из программы введите STOP")
user_word = input("Введите сферу деятельности работодателя[IT компания - рекомендуется]: ").lower()

if user_word in ["", " ", "yes", "true", "it компания", "it", "y", "t"]:
    user_word = "IT компания"


is_stop(user_word)

create_database()
print('Create')
save_data_to_database(user_word)
print('Save')

user_choice = input(f"\nВыберите, что вы хотите получить.\n"
                    f"На текущий момент я могу предложить следующую информацию:\n"
                    f"1 - Список всех компаний и количество вакансий у каждой\n"
                    f"2 - Список всех вакансий с указанием названия компании, "
                    f"названия вакансии, зарплаты и ссылки на компанию\n"
                    f"3 - Среднюю зарплату по вакансиям\n"
                    f"4 - Список всех вакансий, у которых зарплата выше среднего\n"
                    f"5 - Список всех вакансий, в названии которых содержится переданное вами слово\n"
                    f"Для выхода из программы введите STOP\n").upper()

spot_while = True
while spot_while:
    spot_while = check(user_choice)
    if spot_while is True:
        stop_user = input('\nХотите получить больше информации?[yes]: ').lower()
        if stop_user not in ["", " ", "yes", "true", "д", "да", "y", "t"]:
            print('До новых встреч!')
            break
        else:
            user_choice = input('\nКакую информацию желаете увидеть на этот раз?\n')
    else:
        user_choice = input("Пожалуйста, введите одно из предложенных чисел или STOP.\n")
        spot_while = True
