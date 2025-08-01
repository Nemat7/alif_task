import argparse
from datetime import datetime
from database import init_db, check_availability, add_booking
from notification import send_booking_notification
from models import Booking


def parse_datetime(datetime_str: str) -> datetime:
    """Парсинг строки даты и времени"""
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Неправильный формат даты. Используйте YYYY-MM-DD HH:MM")


def check_command(args):
    """Обработка команды проверки"""
    start_time = parse_datetime(f"{args.date} {args.start_time}")
    end_time = parse_datetime(f"{args.date} {args.end_time}")

    result = check_availability(args.cabinet, start_time, end_time)

    if result:
        user_name, end = result
        print(f"Кабинет {args.cabinet} занят {user_name} до {end}")
    else:
        print(f"Кабинет {args.cabinet} свободен с {start_time} до {end_time}")


def book_command(args):
    """Обработка команды бронирования"""
    start_time = parse_datetime(f"{args.date} {args.start_time}")
    end_time = parse_datetime(f"{args.date} {args.end_time}")

    booking = Booking(
        cabinet_number=args.cabinet,
        start_time=start_time,
        end_time=end_time,
        user_name=args.name,
        user_email=args.email,
        user_phone=args.phone
    )

    if add_booking(booking.cabinet_number, booking.start_time, booking.end_time,
                   booking.user_name, booking.user_email, booking.user_phone):
        send_booking_notification(booking)
        print("Кабинет успешно забронирован!")
    else:
        print("Кабинет уже занят в указанное время")


def main():
    """Основная функция CLI"""
    init_db()

    parser = argparse.ArgumentParser(description="Система бронирования кабинетов")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда проверки
    check_parser = subparsers.add_parser("check", help="Проверить доступность кабинета")
    check_parser.add_argument("cabinet", type=int, help="Номер кабинета (1-5)")
    check_parser.add_argument("date", help="Дата (YYYY-MM-DD)")
    check_parser.add_argument("start_time", help="Время начала (HH:MM)")
    check_parser.add_argument("end_time", help="Время окончания (HH:MM)")
    check_parser.set_defaults(func=check_command)

    # Команда бронирования
    book_parser = subparsers.add_parser("book", help="Забронировать кабинет")
    book_parser.add_argument("cabinet", type=int, help="Номер кабинета (1-5)")
    book_parser.add_argument("date", help="Дата (YYYY-MM-DD)")
    book_parser.add_argument("start_time", help="Время начала (HH:MM)")
    book_parser.add_argument("end_time", help="Время окончания (HH:MM)")
    book_parser.add_argument("name", help="Ваше имя")
    book_parser.add_argument("email", help="Ваш email")
    book_parser.add_argument("phone", help="Ваш телефон")
    book_parser.set_defaults(func=book_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
