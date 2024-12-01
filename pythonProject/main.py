import psycopg2
from getpass import getpass


# Подключение к базе данных

connection = psycopg2.connect(
        user="vlanuka",
        password="27062004",
        host="localhost",
        port="5432",
        database="ticket-manager-db"
    )


# Показать доступные мероприятия
def show_events(cursor):
    cursor.execute("""
        SELECT 
            Event.id AS event_id,
            Event.name AS event_name,
            Event.description AS event_description,
            Event.organizer_id AS organizer_id,
            EventSchedule.start_date,
            EventSchedule.end_date,
            EventSchedule.duration,
            EventSchedule.location,
            EventSchedule.description AS eventschedule_description,
            EventSchedule.cost,
            "User".name AS organizer_name
        FROM 
            EventSchedule
        JOIN Event ON EventSchedule.event_id = Event.id
        JOIN "User" ON Event.organizer_id = "User".id
    """)

    events = cursor.fetchall()

    print("\nДоступные мероприятия:")
    for event in events:
        print(f"""
            Event ID: {event[0]}
            Event Name: {event[1]}
            Event Description: {event[2]}
            Organizer ID: {event[3]}
            Start Date: {event[4]}
            End Date: {event[5]}
            Duration: {event[6]}
            Location: {event[7]}
            Event Schedule Description: {event[8]}
            Cost: {event[9]}
            Organizer Name: {event[10]}
        """)


# Добавленная функция show_activity_log
def show_activity_log(cursor, user_id):
    cursor.execute("""
        SELECT 
            ActivityLog.id AS log_id,
            Activity.name AS activity_name,
            ActivityLog.date,
            ActivityLog.time
        FROM 
            ActivityLog
        JOIN Activity ON ActivityLog.activity_id = Activity.id
        WHERE
            ActivityLog.user_id = %s
    """, (user_id,))

    activity_log = cursor.fetchall()

    print("\nЖурнал вашей активности:")
    for log_entry in activity_log:
        print(f"""
            Log ID: {log_entry[0]}
            Activity Name: {log_entry[1]}
            Date: {log_entry[2]}
            Time: {log_entry[3]}
        """)

# Добавление отзыва
def add_review(cursor, user_id):
    # Вывод доступных мероприятий
    show_events(cursor)

    event_id = input("Введите ID мероприятия, для которого хотите добавить отзыв: ")
    content = input("Введите текст отзыва: ")

    # Добавление отзыва
    cursor.execute("""
        INSERT INTO Review (user_id, event_id, content, date, time)
        VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME)
    """, (user_id, event_id, content))

    print("Отзыв успешно добавлен!")

    connection.commit()  # Фиксация изменений в базе данных

#Демонстрация отзывов
def show_reviews(cursor):
    cursor.execute("""
        SELECT 
            Review.id AS review_id,
            "User".name AS user_name,
            Event.name AS event_name,
            Review.content,
            Review.date,
            Review.time
        FROM 
            Review
        JOIN "User" ON Review.user_id = "User".id
        JOIN Event ON Review.event_id = Event.id
    """)

    reviews = cursor.fetchall()

    print("\nОтзывы на все мероприятия:")
    for review in reviews:
        print(f"""
            Review ID: {review[0]}
            User Name: {review[1]}
            Event Name: {review[2]}
            Content: {review[3]}
            Date: {review[4]}
            Time: {review[5]}
        """)


def make_payment(cursor, user_id):
    # Получаем result_cost корзины пользователя
    cursor.execute("""
        SELECT result_cost
        FROM Cart
        WHERE user_id = %s
    """, (user_id,))

    result_cost_row = cursor.fetchone()

    if result_cost_row is not None:
        result_cost = result_cost_row[0]

        # Создаем запись в таблице Payment
        cursor.execute("""
            INSERT INTO Payment (user_id, cart_id, sum, date)
            VALUES (%s, (SELECT id FROM Cart WHERE user_id = %s), %s, CURRENT_DATE)
        """, (user_id, user_id, result_cost))

        print("Платеж успешно совершен!")
    else:
        print("Корзина пользователя пуста. Невозможно совершить платеж.")


    connection.commit()  # Фиксация изменений в базе данных



def show_user_payments(cursor, user_id):
    # Выводим платежи пользователя
    cursor.execute("""
        SELECT 
            id AS payment_id,
            sum,
            date
        FROM 
            Payment
        WHERE
            user_id = %s
    """, (user_id,))

    user_payments = cursor.fetchall()

    if user_payments:
        print("\nПлатежи пользователя:")
        for payment in user_payments:
            print(f"""
                Payment ID: {payment[0]}
                Sum: {payment[1]}
                Date: {payment[2]}
            """)
    else:
        print("\nПлатежей пока не было осуществлено!")


# Добавленная функция show_user_cart
def show_user_cart(cursor, user_id):
    cursor.execute("""
        SELECT 
            Ticket.id AS ticket_id,
            Event.name AS event_name,
            EventSchedule.start_date,
            EventSchedule.location,
            Ticket.ticket_code,
            EventSchedule.cost,
            Cart.result_cost
        FROM 
            Ticket
        JOIN EventSchedule ON Ticket.eventschedule_id = EventSchedule.id
        JOIN Event ON EventSchedule.event_id = Event.id
        LEFT JOIN Cart ON Ticket.user_id = Cart.user_id
        WHERE
            Ticket.user_id = %s
    """, (user_id,))

    user_cart = cursor.fetchall()

    print("\nСодержимое корзины пользователя:")
    for cart_entry in user_cart:
        print(f"""
            Ticket ID: {cart_entry[0]}
            Event Name: {cart_entry[1]}
            Start Date: {cart_entry[2]}
            Location: {cart_entry[3]}
            Ticket Code: {cart_entry[4]}
            Ticket Cost: {cart_entry[5]}
        """)

    if user_cart:  # Проверка, что корзина не пуста
        print(f"""\n--------------------------------\n
            Cart Result Cost: {user_cart[0][6]}""")
    else:
        print("\nКорзина пуста.")


# Регистрация нового пользователя
def register_user(cursor):
    name = input("Введите ваше имя: ")
    email = input("Введите ваш email: ")
    password = input("Введите пароль: ")

    cursor.execute("INSERT INTO \"User\" (name, email, password, role_id) VALUES (%s, %s, %s, %s) RETURNING id",
                   (name, email, password, 1))
    user_id = cursor.fetchone()[0]
    print(f"Пользователь {name} успешно зарегистрирован с ID {user_id}")

    connection.commit()  # Фиксация изменений в базе данных
    return user_id;

# Вход пользователя
def login_user(cursor):
    email = input("Введите ваш email: ")
    password = input("Введите пароль: ")

    cursor.execute("SELECT id FROM \"User\" WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        print(f"Вход успешен! Добро пожаловать, пользователь с ID {user_id}.")
        return user_id
    else:
        print("Неверные email или пароль. Пожалуйста, повторите попытку.")
        return None


# Покупка билета
def buy_ticket(cursor, user_id):
    show_events(cursor)
    event_id = input("Введите ID мероприятия, на которое хотите купить билет: ")

    cursor.execute("INSERT INTO Ticket (eventschedule_id, user_id, ticket_code) VALUES (%s, %s, %s) RETURNING id",
                   (event_id, user_id, 'уникальный_код_билета'))
    ticket_id = cursor.fetchone()[0]
    print(f"Билет куплен успешно с ID {ticket_id}")

    connection.commit()  # Фиксация изменений в базе данных

#Добавление события для организаторов
def add_event(cursor, organizer_id):
    name = input("Введите название мероприятия: ")
    description = input("Введите описание мероприятия: ")

    # Добавление мероприятия
    cursor.execute("""
        INSERT INTO Event (name, description, organizer_id)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, description, organizer_id))

    event_id = cursor.fetchone()[0]

    print(f"Мероприятие успешно добавлено с ID: {event_id}")

    connection.commit()  # Фиксация изменений в базе данных

def show_user_events(cursor, user_id):
    cursor.execute("""
        SELECT id, name, description
        FROM Event
        WHERE organizer_id = %s
    """, (user_id,))

    user_events = cursor.fetchall()

    print("\nВаши мероприятия:")
    for event in user_events:
        print(f"""
            Event ID: {event[0]}
            Event Name: {event[1]}
            Description: {event[2]}
        """)

def add_event_schedule(cursor, event_id):
    start_date = input("Введите дату начала мероприятия в формате YYYY-MM-DD: ")
    end_date = input("Введите дату окончания мероприятия в формате YYYY-MM-DD: ")
    duration = input("Введите продолжительность мероприятия в формате HH:MM: ")
    location = input("Введите место проведения мероприятия: ")
    description = input("Введите описание расписания мероприятия: ")
    cost = float(input("Введите стоимость билета: "))

    # Добавление расписания мероприятия
    cursor.execute("""
        INSERT INTO EventSchedule (event_id, start_date, end_date, duration, location, description, cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (event_id, start_date, end_date, duration, location, description, cost))

    print("Расписание мероприятия успешно добавлено!")

    connection.commit()  # Фиксация изменений в базе данных


def check_user_role(cursor, user_id, role_id):
    cursor.execute("""
        SELECT COUNT(*)
        FROM "User"
        WHERE id = %s AND role_id = %s
    """, (user_id, role_id))

    return cursor.fetchone()[0] > 0

def delete_event_schedule(cursor):
    event_schedule_id = input("Введите ID расписания мероприятия, которое хотите удалить: ")

    # Запрос для удаления расписания мероприятия
    cursor.execute("""
        DELETE FROM EventSchedule
        WHERE id = %s
    """, (event_schedule_id,))

    print("Расписание мероприятия успешно удалено!")

    connection.commit()  # Фиксация изменений в базе данных

    # Обновленная функция edit_event_schedule
def edit_event_schedule(cursor):
        event_schedule_id = input("Введите ID расписания мероприятия, которое хотите отредактировать: ")

        # Запрос для выбора существующего расписания
        cursor.execute("""
            SELECT *
            FROM EventSchedule
            WHERE id = %s
        """, (event_schedule_id,))

        existing_schedule = cursor.fetchone()

        if not existing_schedule:
            print("Расписание мероприятия с указанным ID не найдено.")
            return

        print("Текущие данные расписания мероприятия:")
        print("Event ID:", existing_schedule[1])
        print("Start Date:", existing_schedule[2])
        print("End Date:", existing_schedule[3])
        print("Duration:", existing_schedule[4])
        print("Location:", existing_schedule[5])
        print("Description:", existing_schedule[6])
        print("Cost:", existing_schedule[7])

        # Получаем новые данные для редактирования
        start_date = input(
            "Введите новую дату начала мероприятия в формате YYYY-MM-DD (оставьте пустым для без изменения): ")
        end_date = input(
            "Введите новую дату окончания мероприятия в формате YYYY-MM-DD (оставьте пустым для без изменения): ")
        duration = input(
            "Введите новую продолжительность мероприятия в формате HH:MM (оставьте пустым для без изменения): ")
        location = input("Введите новое место проведения мероприятия (оставьте пустым для без изменения): ")
        description = input("Введите новое описание расписания мероприятия (оставьте пустым для без изменения): ")
        cost = input("Введите новую стоимость билета (оставьте пустым для без изменения): ")

        # Строим SQL-запрос для обновления данных
        update_query = """
            UPDATE EventSchedule
            SET start_date = COALESCE(%s, start_date),
                end_date = COALESCE(%s, end_date),
                duration = COALESCE(%s, duration),
                location = COALESCE(%s, location),
                description = COALESCE(%s, description),
                cost = COALESCE(%s, cost)
            WHERE id = %s
        """

        # Выполняем SQL-запрос с новыми данными
        cursor.execute(update_query, (
        start_date or None, end_date or None, duration or None, location or None, description or None, cost or None,
        event_schedule_id))

        print("Расписание мероприятия успешно отредактировано!")

        connection.commit()  # Фиксация изменений в базе данных

def show_user_schedules(cursor, user_id):
    cursor.execute("""
        SELECT EventSchedule.id, Event.name, EventSchedule.start_date, EventSchedule.end_date, EventSchedule.location
        FROM EventSchedule
        JOIN Event ON EventSchedule.event_id = Event.id
        WHERE Event.organizer_id = %s
    """, (user_id,))

    user_schedules = cursor.fetchall()

    print("\nРасписание мероприятий организатора:")
    for schedule in user_schedules:
        print(f"""
            Schedule ID: {schedule[0]}
            Event Name: {schedule[1]}
            Start Date: {schedule[2]}
            End Date: {schedule[3]}
            Location: {schedule[4]}
        """)

def show_all_users(cursor):
    cursor.execute("""
        SELECT "User".id, "User".name, "User".email, "User".role_id, Role.name AS role_name
        FROM "User"
        LEFT JOIN Role ON "User".role_id = Role.id
    """)
    all_users = cursor.fetchall()

    print("\nСписок всех пользователей:")
    for user in all_users:
        print(f"""
            User ID: {user[0]}
            Name: {user[1]}
            Email: {user[2]}
            Role ID: {user[3]}
            Role Name: {user[4]}
        """)

def edit_user(cursor):
    user_id_to_edit = input("Введите ID пользователя, данные которого хотите отредактировать: ")

    # Запрос для выбора существующего пользователя
    cursor.execute("""
        SELECT *
        FROM "User"
        WHERE id = %s
    """, (user_id_to_edit,))

    existing_user = cursor.fetchone()

    if not existing_user:
        print("Пользователь с указанным ID не найден.")
        return

    print("Текущие данные пользователя:")
    print("Name:", existing_user[1])
    print("Email:", existing_user[2])
    print("Role ID:", existing_user[4])

    # Получаем новые данные для редактирования
    new_name = input("Введите новое имя пользователя (оставьте пустым для без изменения): ")
    new_email = input("Введите новый email пользователя (оставьте пустым для без изменения): ")
    new_role_id = input("Введите новый role_id пользователя (оставьте пустым для без изменения): ")

    # Строим SQL-запрос для обновления данных
    update_query = """
        UPDATE "User"
        SET name = COALESCE(%s, name),
            email = COALESCE(%s, email),
            role_id = COALESCE(%s, role_id)
        WHERE id = %s
    """

    # Выполняем SQL-запрос с новыми данными
    cursor.execute(update_query, (new_name or None, new_email or None, new_role_id or None, user_id_to_edit))

    print("Данные пользователя успешно отредактированы!")

    connection.commit()  # Фиксация изменений в базе данных

def delete_user(cursor):
    user_id_to_delete = input("Введите ID пользователя, которого хотите удалить: ")

    # Удаление записей из ActivityLog связанных с удаляемым пользователем
    cursor.execute("""
        DELETE FROM ActivityLog
        WHERE user_id = %s
    """, (user_id_to_delete,))

    # Запрос для удаления пользователя
    cursor.execute("""
        DELETE FROM "User"
        WHERE id = %s
    """, (user_id_to_delete,))

    print("Пользователь успешно удален!")

    connection.commit()  # Фиксация изменений в базе данных



# Основная функция приложения
def main():
    if not connection:
        return

    user_id = None  # Идентификатор пользователя для текущей сессии

    try:
        with connection.cursor() as cursor:
            while True:
                print("\n=== Менеджер билетов мероприятий ===")
                print("1. Просмотреть доступные мероприятия")
                print("2. Зарегистрироваться")
                print("3. Войти")
                print("4. Добавить билет в корзину")
                print("5. Показать мой журнал активности")
                print("6. Показать содержимое корзины")
                print("7. Совершить платеж")
                print("8. Показать платежи пользователя")
                print("9. Написать отзыв")
                print("10. Показать отзывы")

                if (check_user_role(cursor, user_id, 2) or check_user_role(cursor, user_id, 3)):
                    print("11. Добавить мероприятие")
                    print("12. Мои мероприятия")
                    print("13. Добавить афишу на мероприятие")
                    print("14. Редактировать афишу на мероприятие")
                    print("15. Удалить афишу на мероприятие")

                if (check_user_role(cursor, user_id, 3)):
                    print("16. Список всех пользователей")
                    print("17. Редактировать пользователя")

                print("0. Выйти")

                choice = input("Выберите действие: ")

                if choice == "1":
                    show_events(cursor)
                elif choice == "2":
                    register_user(cursor)
                elif choice == "3":
                    user_id = login_user(cursor)
                elif choice == "4":
                    if user_id:
                        buy_ticket(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "5":
                    if user_id:
                        show_activity_log(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "6":
                    if user_id:
                        show_user_cart(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "7":
                    if user_id:
                        make_payment(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "8":
                    if user_id:
                        show_user_payments(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "9":
                    if user_id:
                        add_review(cursor, user_id)
                    else:
                        print("Сначала войдите в систему.")
                elif choice == "10":
                    show_reviews(cursor)
                elif choice == "11":
                    if user_id and check_user_role(cursor, user_id, 2):
                        add_event(cursor, user_id)
                    else:
                        print("У вас нет прав для выполнения этой операции.")
                elif choice == "12":
                        show_user_events(cursor, user_id)
                elif choice == "13":
                    show_user_events(cursor, user_id)
                    event_id = input("Введите ID мероприятия, для которого хотите добавить расписание: ")
                    add_event_schedule(cursor, event_id)
                elif choice == "14":
                        show_user_schedules(cursor, user_id)
                        edit_event_schedule(cursor)
                elif choice == "15":
                        show_user_schedules(cursor, user_id)
                        delete_event_schedule(cursor)
                elif choice == "16":
                        show_all_users(cursor)
                elif choice == "17":
                        show_all_users(cursor)
                        edit_user(cursor)
                elif choice == "0":
                    print("Выход из приложения.")
                    break
                else:
                    print("Некорректный выбор. Пожалуйста, введите корректное значение.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()