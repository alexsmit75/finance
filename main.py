import uuid
from typing import List, Dict, Optional
import os
import csv

# Путь к файлу с данными финансов
data_file: str = 'finances.csv'

def check_and_create_file() -> None:
    """
    Проверяет наличие файла данных и создает его, если он не существует.
    """
    if not os.path.isfile(data_file):
        print(f"Файл {data_file} не найден. Создаем новый файл.")
        with open(data_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ['id', 'date', 'type', 'amount', 'category', 'description']
            writer.writerow(headers)
    else:
        print(f"Файл {data_file} уже существует.")

def read_data() -> List[Dict[str, str]]:
    """
    Читает данные из CSV-файла и возвращает их в виде списка словарей.

    Returns:
        List[Dict[str, str]]: Список словарей с данными финансов.
    """
    with open(data_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_data(finances: List[Dict[str, str]]) -> None:
    """
    Записывает данные в CSV-файл.

    Args:
        finances (List[Dict[str, str]]): Список словарей с данными для записи.
    """
    with open(data_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=finances[0].keys())
        writer.writeheader()
        writer.writerows(finances)

def save_last_id(last_id: int) -> None:
    """
    Сохраняет последний использованный идентификатор в файл.

    Args:
        last_id (int): Последний использованный идентификатор.
    """
    with open('last_id.txt', mode='w', encoding='utf-8') as file:
        file.write(str(last_id))

def load_last_id() -> int:
    """
    Загружает последний использованный идентификатор из файла.

    Returns:
        int: Загруженный идентификатор.
    """
    try:
        with open('last_id.txt', mode='r', encoding='utf-8') as file:
            return int(file.read())
    except FileNotFoundError:
        return 1  # Если файл не найден, начинаем с 1

def get_next_id() -> int:
    """
    Получает следующий уникальный идентификатор для новой записи.

    Returns:
        int: Следующий идентификатор.
    """
    return load_last_id() + 1

def add_entry() -> None:
    """
    Добавляет новую запись в файл данных.
    """
    entry_id = get_next_id()
    date: str = input("Введите дату (ГГГГ-ММ-ДД): ")
    entry_type: str = input("Введите тип (доход/расход): ")
    amount: str = input("Введите сумму: ")
    category: str = input("Введите категорию: ")
    description: str = input("Введите описание: ")

    new_entry: Dict[str, str] = {
        'id': str(entry_id),
        'date': date,
        'type': entry_type,
        'amount': amount,
        'category': category,
        'description': description
    }

    finances: List[Dict[str, str]] = read_data()
    finances.append(new_entry)
    write_data(finances)
    save_last_id(entry_id)
    print("Запись добавлена.")

def search_by_id(entry_id: str) -> Optional[Dict[str, str]]:
    """
    Ищет запись по идентификатору.

    Args:
        entry_id (str): Идентификатор записи для поиска.

    Returns:
        Optional[Dict[str, str]]: Найденная запись или None, если запись не найдена.
    """
    finances: List[Dict[str, str]] = read_data()
    for entry in finances:
        if entry['id'] == entry_id:
            return entry
    return None

def show_all_ids() -> None:
    """
    Выводит все идентификаторы записей.
    """
    finances: List[Dict[str, str]] = read_data()
    print("Все доступные ID:")
    for entry in finances:
        print(entry['id'])

def edit_entry(entry_id: str) -> None:
    """
    Редактирует существующую запись по идентификатору.

    Args:
        entry_id (str): Идентификатор записи для редактирования.
    """
    finances = read_data()
    entry = search_by_id(entry_id)
    if entry:
        print("Текущие данные записи:", entry)
        new_date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
        entry['date'] = new_date if new_date else entry['date']
        new_type = input("Введите новый тип (доход/расход): ")
        entry['type'] = new_type if new_type else entry['type']
        new_amount = input("Введите новую сумму: ")
        entry['amount'] = new_amount if new_amount else entry['amount']
        new_category = input("Введите новую категорию: ")
        entry['category'] = new_category if new_category else entry['category']
        new_description = input("Введите новое описание: ")
        entry['description'] = new_description if new_description else entry['description']

        for i, e in enumerate(finances):
            if e['id'] == entry_id:
                finances[i] = entry
                break

        write_data(finances)
        print("Запись обновлена.")
    else:
        print("Запись с таким ID не найдена.")
        show_all_ids()

def main() -> None:
    """
    Главная функция программы.
    """
    check_and_create_file()
    while True:
        print("\nЛичный финансовый кошелек")
        print("1. Добавить запись")
        print("2. Найти запись по ID")
        print("3. Редактировать запись")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            add_entry()
        elif choice == '2':
            entry_id = input("Введите ID записи для поиска: ")
            entry = search_by_id(entry_id)
            if entry:
                print("Найденная запись:", entry)
            else:
                print("Запись не найдена.")
                show_all_ids()
        elif choice == '3':
            entry_id = input("Введите ID записи для редактирования: ")
            edit_entry(entry_id)
        elif choice == '4':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
