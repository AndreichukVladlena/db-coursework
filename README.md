##Система онлайн-регистрации и управления мероприятиями

##Андрейчук Владлена Витальевна, 153501

## Сущности

* ```User``` 
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + name VARCHAR(50) NOT NULL,
    + email VARCHAR(50) UNIQUE NOT NULL,
    + password VARCHAR(255) NOT NULL,
    + role VARCHAR(50) NOT NULL
  
* ```Event```
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + name VARCHAR(100) NOT NULL,
    + description TEXT,
    + image VARCHAR(255),
    + organizer_id BIGINT REFERENCES user(id) NOT NULL
  
* ```Ticket```
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + event_id BIGINT REFERENCES event(id) NOT NULL,
    + participant_id BIGINT REFERENCES user(id) NOT NULL,
    + ticket_code VARCHAR(50) NOT NULL
  
* ```EventSchedule```
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + event_id BIGINT REFERENCES event(id) NOT NULL,
    + start_date DATE NOT NULL,
    + end_date DATE NOT NULL,
    + time TIME NOT NULL,
    + location VARCHAR(100) NOT NULL,
    + description TEXT
  
* ```ActivityLog``` 
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + user_id BIGINT REFERENCES user(id) NOT NULL,
    + event_id BIGINT REFERENCES event(id),
    + timestamp TIMESTAMP NOT NULL,
    + description TEXT
  
* ```Role``` 
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + name VARCHAR(50) UNIQUE NOT NULL
  
* ```EventCategory```
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + name VARCHAR(50) UNIQUE NOT NULL
  
* ```Review```
  
    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + user_id BIGINT REFERENCES user(id) NOT NULL,
    + event_id BIGINT REFERENCES event(id) NOT NULL,
    + text TEXT NOT NULL,
    + timestamp TIMESTAMP NOT NULL
  
* ```EventImage``` 

    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + event_id BIGINT REFERENCES event(id) NOT NULL,
    + image_path VARCHAR(255),
    + description TEXT,
    + upload_date TIMESTAMP NOT NULL
  
* ```Payment```

    + id BIGSERIAL PRIMARY KEY NOT NULL,
    + user_id BIGINT REFERENCES user(id) NOT NULL,
    + ticket_id BIGINT REFERENCES ticket(id) NOT NULL,
    + amount DECIMAL NOT NULL,
    + payment_date TIMESTAMP NOT NULL  


## Функциональные требования к системе онлайн-регистрации и управления мероприятиями
* 1. **Авторизация и аутентификация**
    + 1.1 Вход в систему

            Система должна предоставлять возможность пользователям (организаторам мероприятий и участникам) войти в систему с использованием уникальных учетных данных (логин и пароль).

    + 1.2 Регистрация новых пользователей

            Система должна позволять новым пользователям создавать учетные записи путем предоставления необходимой информации, включая имя, адрес электронной почты и пароль.

    + 1.3 Восстановление пароля

            Пользователи должны иметь возможность сбросить свой пароль через отправку ссылки для восстановления на указанный адрес электронной почты.

* 2. **Управление мероприятиями**

    + 2.1 Создание мероприятий

            Организаторы мероприятий должны иметь возможность создавать новые мероприятия, указывая информацию, такую как название, дата, время, местоположение и описание.

    + 2.2 Редактирование мероприятий

            Организаторы мероприятий должны иметь возможность редактировать информацию о созданных мероприятиях.

    + 2.3 Удаление мероприятий

            Организаторы мероприятий должны иметь возможность удалять мероприятия, которые больше не актуальны.

* 3. **Управление расписанием**
  
    + 3.1 Добавление событий в расписание

            Организаторы мероприятий должны иметь возможность добавлять события (например, семинары, выступления) в расписание мероприятия, указывая дату, время и место проведения.

    + 3.2 Редактирование событий

            Организаторы мероприятий должны иметь возможность редактировать информацию о событиях в расписании.

    + 3.3 Удаление событий

            Организаторы мероприятий должны иметь возможность удалять события из расписания.

* 4. **Управление билетами**
    + 4.1 Генерация билетов

            После успешной регистрации на мероприятие, участникам должны генерироваться билеты в электронном виде с уникальными штрих-кодами или QR-кодами.

    + 4.2 Просмотр билетов

            Участники и организаторы мероприятий должны иметь возможность просматривать информацию о своих билетах, включая детали мероприятия и код билета.

* 5. **Система ролей**
  
    + 5.1 Роли пользователей

            Система должна поддерживать следующие роли пользователей: администратор, организатор мероприятий и участник.

    + 5.2 Права доступа

            Каждая роль должна иметь определенные права доступа, например, администратор имеет полный доступ к управлению системой, организатор может создавать и управлять мероприятиями, а участник может регистрироваться на мероприятия и просматривать свои билеты.

* 6. **Журналирование действий пользователя**
   
    + 6.1 Журналирование событий

            Система должна вести журнал действий пользователей, включая вход и выход из системы, создание и редактирование мероприятий, регистрацию на мероприятия и другие важные события.

    + 6.2 Хранение журнала

            Журнал должен храниться в безопасной и защищенной базе данных для последующего анализа и мониторинга.


## Схема БД
![Alt text](<Диаграмма без названия.drawio.png>)
