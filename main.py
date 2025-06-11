import datetime
import json
import os

# Шлях до файлу з подіями
EVENTS_FILE = "events.json"

# Завантаження подій з файлу
def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Збереження подій до файлу
def save_events(events):
    with open(EVENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

# Вивід вітання
def greet_user():
    print("Привіт! Я бот-організатор. Допоможу тобі керувати подіями.")
    print("Введи 'допомога', щоб побачити доступні команди.")

# Вивід списку команд
def show_help():
    print("\nДоступні команди:")
    print("допомога - список команд")
    print("додати подію - додати нову подію")
    print("показати події - показати всі події")
    print("події на тиждень - події цього тижня")
    print("пошук за категорією - пошук подій за категорією")
    print("видалити подію - видалити подію за назвою і датою")
    print("вийти - вихід з програми\n")

# Додавання події
def add_event(events):
    name = input("Введи назву події: ")
    date_str = input("Введи дату (рррр-мм-дд): ")
    category = input("Введи опис або категорію: ")
    try:
        # Перевірка коректності дати
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        events.append({"name": name, "date": date_str, "category": category})
        save_events(events)
        print("Подію додано!")
    except ValueError:
        print("Некоректна дата. Спробуй ще раз.")

# Показ усіх подій
def show_all_events(events):
    if not events:
        print("Подій немає.")
        return
    print("\nУсі події:")
    for event in events:
        print(f"- {event['name']} | {event['date']} | {event['category']}")
    print()

# Події на поточний тиждень
def events_this_week(events):
    today = datetime.date.today()
    week_later = today + datetime.timedelta(days=7)
    found = False
    print("\nПодії на цей тиждень:")
    for event in events:
        try:
            event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= week_later:
                print(f"- {event['name']} | {event['date']} | {event['category']}")
                found = True
        except ValueError:
            continue
    if not found:
        print("Немає подій на цей тиждень.")
    print()

# Пошук подій за категорією
def search_by_category(events):
    keyword = input("Введи назву категорії або ключове слово: ").lower()
    found = False
    print("\nРезультати пошуку:")
    for event in events:
        if keyword in event["category"].lower():
            print(f"- {event['name']} | {event['date']} | {event['category']}")
            found = True
    if not found:
        print("Подій не знайдено.")
    print()

# Видалення події
def delete_event(events):
    name = input("Введи назву події для видалення: ")
    date_str = input("Введи дату події (рррр-мм-дд): ")
    initial_count = len(events)
    events = [event for event in events if not (event["name"] == name and event["date"] == date_str)]
    if len(events) < initial_count:
        save_events(events)
        print("Подію видалено.")
    else:
        print("Подію не знайдено.")
    return events

# Основний цикл програми
def main():
    events = load_events()
    greet_user()
    while True:
        command = input(">>> ").strip().lower()
        if command == "допомога":
            show_help()
        elif command == "додати подію":
            add_event(events)
        elif command == "показати події":
            show_all_events(events)
        elif command == "події на тиждень":
            events_this_week(events)
        elif command == "пошук за категорією":
            search_by_category(events)
        elif command == "видалити подію":
            events = delete_event(events)
        elif command == "вийти":
            print("До зустрічі!")
            break
        else:
            print("Невідома команда. Введи 'допомога', щоб побачити доступні команди.")

# Запуск програми
if __name__ == "__main__":
    main()
