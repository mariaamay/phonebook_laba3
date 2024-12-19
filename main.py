import json
import re
from datetime import datetime

# Имя файла для хранения данных
FILE_NAME = "contacts.json"

def load_contacts():
    """Загрузка данных из файла."""
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_contacts(data):
    """Сохранение данных в файл."""
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def validate_name(name):
    """Проверка имени и фамилии."""
    pattern = r'^[a-zA-Z0-9 ]+$'
    return bool(re.match(pattern, name))

def validate_phone(number):
    """Проверка формата номера телефона."""
    return len(number) == 11 and number.isdigit() and number[0] == "8"

def validate_dob(dob):
    """Проверка формата даты рождения."""
    if dob == "":
        return True
    else:
        try:
            datetime.strptime(dob, "%d.%m.%Y")
            return True
        except ValueError:
            return False

def input_id():
    """Создание идентификатора (имя + фамилия)."""
    name = input("Введите имя: ").strip().capitalize()
    if not validate_name(name):
        print("Некорректное имя. Убедитесь, что оно содержит только латинские буквы, цифры и пробелы\n")
        return

    surname = input("Введите фамилию: ").strip().capitalize()
    if not validate_name(surname):
        print("Некорректная фамилия. Убедитесь, что она содержит только латинские буквы, цифры и пробелы\n")
        return
    identifier = f'{name} {surname}'
    return identifier

def add_record(phonebook):
    """Добавление контакта"""
    name = input("Введите имя: ").strip().capitalize()
    if not validate_name(name):
        print("Некорректное имя. Убедитесь, что оно содержит только латинские буквы, цифры и пробелы")
        return

    surname = input("Введите фамилию: ").strip().capitalize()
    if not validate_name(surname):
        print("Некорректная фамилия. Убедитесь, что она содержит только латинские буквы, цифры и пробелы")
        return
    identifier = f'{name} {surname}'

    if identifier in phonebook:
        print("Запись с таким именем и фамилией уже существует")
        print("Доступные опции: ")
        print("1. Изменить существующую запись")
        print("2. Изменить имя и фамилию новой записи")
        print("3. Вернуться к выбору команды")

        command = input("Введите номер желаемой операции: ")
        if command == '1':
            edit_contact_by_id(phonebook, identifier)
            return
        elif command == '2':
            add_record(phonebook)
            return
        elif command == '3':
            return
        else:
            print("Некорректный номер операции. Введите цифру от 1 до 3")

    phone = input("Введите номер телефона (11 цифр, начинается в +7 или 8): ").strip()
    if phone.startswith("+7"):
        phone = "8" + phone[2:]
    if not validate_phone(phone):
        print("Некорректный номер телефона. Убедитесь, что он начинается с +7 или 8 и содержит только 11 цифр")
        return

    dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
    if not validate_dob(dob):
        print("Некорректная дата рождения. Убедитесь, что формат дд.мм.гггг")
        return

    phonebook[identifier] = {
        'phone': phone,
        'date_of_birth': dob
    }
    print(f'Запись для {identifier} добавлена.')
    save_contacts(phonebook)

def delete_contact(phonebook):
    """Удаление контакта по идентификатору (имя + фамилия)."""
    identifier = input_id()
    if identifier not in phonebook:
        print("Контакт не найден.")
        return
    phonebook.pop(identifier)
    print(f'Запись {identifier} успешно удалена.')
    save_contacts(phonebook)

def search(phonebook):
    """Поиск контактов в телефонной книге."""
    print("Доступные варианты поиска: ")
    print("1. Имя")
    print("2. Фамилия")
    print("3. Имя и фамилия")
    print("4. Номер телефона")
    print("5. Дата рождения")

    command = input("Введите номер поля, по которому осуществить поиск: ")
    results = []
    if command == '3':
        results.append(search_by_id(phonebook))
    elif command == '1':
        name = input("Введите имя для поиска: ").strip().capitalize()
        if not validate_name(name):
            print("Некорректное имя. Убедитесь, что оно содержит только латинские буквы, цифры и пробелы")
            return []
        results = [f"{id}: {data['phone']} {data['date_of_birth']}" for id, data in phonebook.items() if id.split(" ")[0] == name]
    elif command == '2':
        surname = input("Введите фамилию для поиска: ").strip().capitalize()
        if not validate_name(surname):
            print("Некорректная фамилия. Убедитесь, что она содержит только латинские буквы, цифры и пробелы")
            return []
        results = [f"{id}: {data['phone']} {data['date_of_birth']}" for id, data in phonebook.items() if id.split(" ")[1] == surname]
    elif command == '4':
        phone = input("Введите номер телефона (11 цифр, начинается в +7 или 8): ").strip()
        if not validate_phone(phone):
            print("Некорректный номер телефона. Убедитесь, что он начинается с +7 или 8 и содержит только 11 цифр")
            return []
        results = [f"{id}: {data['phone']} {data['date_of_birth']}" for id, data in phonebook.items() if data['phone'] == phone]
    elif command == '5':
        dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
        if not validate_dob(dob):
            print("Некорректная дата рождения. Убедитесь, что формат дд.мм.гггг")
            return []
        results = [f"{id}: {data['phone']} {data['date_of_birth']}" for id, data in phonebook.items() if data['date_of_birth'] == dob]
    else:
        print("Несуществующее поле. Введите цифру от 1 до 5: ")
        return []

    return results
def search_contacts(phonebook):
    """Вывод результатов поиска контактов в телефонной книге."""
    results = search(phonebook)
    if results:
        print("Найденные записи:")
        for res in results:
            print(res)
    else:
        print("Контакты не найдены.")
def search_by_id(phonebook):
    """Поиск контакта по идентификатору (имя + фамилия)."""
    identifier = input_id()
    if identifier not in phonebook:
        print("Контакт не найден.")
        return None
    return f"{identifier}: {phonebook[identifier]['phone']} {phonebook[identifier]['date_of_birth']}"

def edit_contact(phonebook):
    """Редактирование контакта по идентификатору (имя + фамилия)."""
    identifier = input_id()
    if identifier not in phonebook:
        print("Контакт не найден.")
        return
    edit_contact_by_id(phonebook, identifier)

def edit_contact_by_id(phonebook, identifier):
    """Редактирование контакта."""
    print("Доступны к редактированию: ")
    print("1. Имя")
    print("2. Фамилия")
    print("3. Номер телефона")
    print("4. Дата рождения")

    command = input("Введите номер поля, которое вы хотите изменить: ")
    if command == '1':
        new_name = input("Введите новое имя: ").strip().capitalize()
        if not validate_name(new_name):
            print("Некорректное имя. Убедитесь, что оно содержит только латинские буквы, цифры и пробелы")
            return

        new_identifier = f'{new_name} {identifier.split(" ")[1]}'
        if new_identifier in phonebook:
            print("Запись с таким именем и фамилией уже существует")
            return

        phonebook[new_identifier] = {
            'phone': phonebook[identifier]['phone'],
            'date_of_birth': phonebook[identifier]['date_of_birth']
        }
        phonebook.pop(identifier)

    elif command == '2':
        new_surname = input("Введите новую фамилию: ").strip().capitalize()
        if not validate_name(new_surname):
            print("Некорректная фамилия. Убедитесь, что она содержит только латинские буквы, цифры и пробелы")
            return
        new_identifier = f'{identifier.split(" ")[0]} {new_surname}'
        if new_identifier in phonebook:
            print("Запись с таким именем и фамилией уже существует")
            return

        phonebook[new_identifier] = {
            'phone': phonebook[identifier]['phone'],
            'date_of_birth': phonebook[identifier]['date_of_birth']
        }
        phonebook.pop(identifier)

    elif command == '3':
        new_phone = input("Введите номер телефона (11 цифр, начинается в +7 или 8): ").strip()
        if not validate_phone(new_phone):
            print("Некорректный номер телефона. Убедитесь, что он начинается с +7 или 8 и содержит только 11 цифр")
            return
        phonebook[identifier] = {
            'phone': new_phone,
            'date_of_birth': phonebook[identifier]['date_of_birth']
        }

    elif command == '4':
        new_dob = input("Введите новую дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
        if not validate_dob(new_dob):
            print("Некорректная дата рождения. Убедитесь, что формат дд.мм.гггг")
            return

        phonebook[identifier] = {
             'phone': phonebook[identifier]['phone'],
            'date_of_birth': new_dob
        }
    else:
        print("Несуществующее поле. Введите цифру от 1 до 4: ")

    print(f'Запись {identifier} успешно отредактирована.')
    save_contacts(phonebook)

def calculateAge(phonebook):
    """Вывод возраста контакта по идентификатору (имя + фамилия)."""
    identifier = input_id()
    if identifier not in phonebook:
        print("Контакт не найден.")
        return
    if phonebook[identifier]['date_of_birth'] == "":
        print("Дата рождения пуста. Невозможно вычислить возраст.")
        return 0
    dob = datetime.strptime(phonebook[identifier]['date_of_birth'], '%d.%m.%Y')
    difference = datetime.now() - dob
    age = difference.days // 365
    return age

def display_contacts(phonebook):
    """Вывод информации о всех существующих контактах в телефонной книге."""
    if not phonebook:
        print("Телефонная книга пуста.\n")
        return

    for id, data in phonebook.items():
        print(f"{id}: {data['phone']} {data['date_of_birth']}")


def main():
    phonebook = load_contacts()
    while True:
        print("Доступные операции:")
        print("1. Открыть телефонную книгу.")
        print("2. Добавить контакт.")
        print("3. Удалить контакт.")
        print("4. Найти контакт.")
        print("5. Редактировать контакт.")
        print("6. Вычислить возраст контакта.")
        print("Для завершения работы введите 'quit'")
        command = input("Введите номер операции: ").strip()

        if command == '1':
            display_contacts(phonebook)
        elif command == '2':
            add_record(phonebook)
        elif command == '3':
            delete_contact(phonebook)
        elif command == '4':
            search_contacts(phonebook)
        elif command == '5':
            edit_contact(phonebook)
        elif command == '6':
            age = calculateAge(phonebook)
            if age == 0:
                continue
            print(f'Возраст: {age}')
        elif command == "quit":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Введите номер команды от 1 до 6 или 'quit' для завершения работы программы")

if __name__ == "__main__":
    main()