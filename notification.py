def send_email_notification(email: str, message: str):
    #Имитируем отправку на почту
    print(f"Отправка email на {email}: {message}")

def send_sms_notification(phone: str, message: str):
    # Имитируем отправку по СМС
    print(f"Отправка СМС на {phone}: {message}")

def send_booking_notification(booking):
    # Отправка уведомлений о бронировании
    message = (f"Вы забронировали кабинет {booking.cabinet_number}"
               f"с {booking.start_time} до {booking.end_time}")

    send_email_notification(booking.user_email, message)
    send_sms_notification(booking.user_phone, message)