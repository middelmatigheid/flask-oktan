import os
import datetime
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Connecting to the database
HOST = os.getenv('HOST')
DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
connection = psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD, port=PORT)


# Deleting all tables
def delete_tables():
    with connection.cursor() as cursor:
        cursor.execute("""DROP TABLE IF EXISTS subdivisions, coaches, schedules, news, admins, logs;""")
        connection.commit()


# Creating tables if they don't exist
def create_tables():
    with connection.cursor() as cursor:
        # Table stores admins
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS admins(
                admin_login TEXT PRIMARY KEY,
                admin_password TEXT
                );""")

        # Table stores logs
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS logs(
                log_id serial PRIMARY KEY,
                admin_login TEXT,
                log_date TEXT,
                log_text TEXT
                );""")

        # Table stores subdivisions' names
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS subdivisions(
                subdivision_id serial PRIMARY KEY,
                subdivision_name TEXT
                );""")

        # Table stores coaches
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS coaches(
                coach_id serial PRIMARY KEY,
                coach_subdivision TEXT,
                coach_name TEXT,
                coach_info TEXT,
                coach_phone TEXT,
                coach_address TEXT
                );""")
        connection.commit()

        # Table stores schedules
        # Schedule_format stores schedule's image format
        # Schedule_position stores schedule's position on the page
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS schedules(
                schedule_id serial PRIMARY KEY,
                schedule_position INTEGER
                );""")

        # Table stores news
        # News_date is in format %d-%m-%Y %H:%M
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS news(
                news_id serial PRIMARY KEY,
                news_date TEXT,
                news_title TEXT,
                news_text TEXT
                );""")


# Adding new admin
def add_admin(admin_login, admin_password):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO admins (admin_login, admin_password) VALUES ('{admin_login}', '{admin_password}');""")
        connection.commit()


# Adding new log
def add_log(admin_login, log_date, log_text):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO logs (admin_login, log_date, log_text) VALUES ('{admin_login}', '{log_date}', '{log_text}');""")
        connection.commit()


# Adding new subdivision
def add_subdivision(subdivision_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO subdivisions (subdivision_name) VALUES ('{subdivision_name}');""")
        connection.commit()


# Adding new coach, returning his coach_id
def add_coach(coach_subdivision, coach_name, coach_info, coach_phone, coach_address):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO coaches (coach_subdivision, coach_name, coach_info, coach_phone, coach_address) VALUES ('{coach_subdivision}', '{coach_name}', '{coach_info}', '{coach_phone}', '{coach_address}');""")
        connection.commit()
        cursor.execute(f"""SELECT coach_id FROM coaches WHERE coach_subdivision = '{coach_subdivision}' AND coach_name = '{coach_name}' AND coach_info = '{coach_info}' AND coach_phone = '{coach_phone}' AND coach_address = '{coach_address}';""")
        coach_id = cursor.fetchone()
        if coach_id is not None:
            coach_id = coach_id[0]
        return coach_id


# Adding new schedule, returning its schedule_id
def add_schedule(schedule_position):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO schedules (schedule_position) VALUES ({schedule_position});""")
        connection.commit()
        cursor.execute(f"""SELECT schedule_id FROM schedules WHERE schedule_position = {schedule_position};""")
        schedule_id = cursor.fetchone()
        if schedule_id is not None:
            schedule_id = schedule_id[0]
        return schedule_id


# Addnig new news, returning its news_id
def add_news(news_date, news_title, news_text):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO news (news_date, news_title, news_text) VALUES ('{news_date}', '{news_title}', '{news_text}');""")
        connection.commit()
        cursor.execute(f"""SELECT news_id FROM news WHERE news_date = '{news_date}' AND news_title = '{news_title}' AND news_text = '{news_text}';""")
        news_id = cursor.fetchone()
        if news_id is not None:
            news_id = news_id[0]
        return news_id


# Updating coach
def update_coach(coach_id, coach_subdivision, coach_name, coach_info, coach_phone, coach_address):
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE coaches SET coach_subdivision = '{coach_subdivision}', coach_name = '{coach_name}', coach_info = '{coach_info}', coach_phone = '{coach_phone}', coach_address = '{coach_address}' WHERE coach_id = {coach_id}""")
        connection.commit()


# Updating schedule's position
def update_schedule_position(schedule_id, schedule_position):
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE schedules SET schedule_position = {schedule_position} WHERE schedule_id = {schedule_id};""")
        connection.commit()


# Updating news
def update_news(news_id, news_title, news_text):
    with connection.cursor() as cursor:
        cursor.execute(f"""UPDATE news SET news_title = '{news_title}', news_text = '{news_text}' WHERE news_id = {news_id};""")
        connection.commit()


# Deleting admin
def delete_admin(admin_login):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM admins WHERE admin_login = '{admin_login}';""")
        connection.commit()


# Deleting log
def delete_log(log_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM logs WHERE log_id = {log_id};""")
        connection.commit()


# Deleting subdivision
def delete_subdivision(subdivision_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM subdivisions WHERE subdivision_id = {subdivision_id};""")
        connection.commit()


# Deleting coach
def delete_coach(coach_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM coaches WHERE coach_id = {coach_id};""")
        connection.commit()


# Deleting schedule
def delete_schedule(schedule_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM schedules WHERE schedule_id = {schedule_id};""")
        connection.commit()


# Deleting news
def delete_news(news_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM news WHERE news_id = {news_id};""")
        connection.commit()


# Getting all admins
def get_admins():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM admins;""")
        admins = cursor.fetchall()
        if admins is not None:
            admins_arr = []
            for admin in admins:
                admin_keys = ['admin_login', 'admin_password']
                admin_dict = {}
                for i in range(len(admin_keys)):
                    admin_dict[admin_keys[i]] = admin[i]
                admins_arr.append(admin_dict)
            admins = admins_arr
        return admins


# Getting admin by his admin_login
def get_admin_by_login(admin_login):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM admins WHERE admin_login = '{admin_login}';""")
        admin = cursor.fetchone()
        if admin is not None:
            admin_keys = ['admin_login', 'admin_password']
            admin_dict = {}
            for i in range(len(admin_keys)):
                admin_dict[admin_keys[i]] = admin[i]
            admin = admin_dict
        return admin


# Getting all logs
def get_logs():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM logs;""")
        logs = cursor.fetchall()
        if logs is not None:
            logs_arr = []
            for log in logs:
                log_keys = ['log_id', 'admin_login', 'log_date', 'log_text']
                log_dict = {}
                for i in range(len(log_keys)):
                    log_dict[log_keys[i]] = log[i]
                log_dict['log_date'] = datetime.datetime.strptime(log_dict['log_date'], '%d-%m-%Y %H:%M').strftime('%d-%m-%Y %H:%M')
                # Deleting logs that older than 100 days
                if (datetime.datetime.now() - datetime.datetime.strptime(log_dict['log_date'], '%d-%m-%Y %H:%M')).days <= 100:
                    logs_arr.append(log_dict)
                else:
                    delete_log(log_dict['log_id'])
            logs = sorted(logs_arr, key=lambda x: x['log_date'], reverse=True)
        return logs


# Getting all subdivisions
def get_subdivisions():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM subdivisions;""")
        subdivisions = cursor.fetchall()
        if subdivisions is not None:
            subdivisions_arr = []
            for subdivision in subdivisions:
                subdivision_keys = ['subdivision_id', 'subdivision_name']
                subdivision_dict = {}
                for i in range(len(subdivision_keys)):
                    subdivision_dict[subdivision_keys[i]] = subdivision[i]
                subdivisions_arr.append(subdivision_dict)
            subdivisions = subdivisions_arr
        return subdivisions


# Getting all coaches in the specific subdivision
def get_coaches_by_subdivision(coach_subdivision):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM coaches WHERE coach_subdivision = '{coach_subdivision}';""")
        coaches = cursor.fetchall()
        if coaches is not None:
            coaches_arr = []
            for coach in coaches:
                coach_keys = ['coach_id', 'coach_subdivision', 'coach_name', 'coach_info', 'coach_phone', 'coach_address']
                coach_dict = {}
                for i in range(len(coach_keys)):
                    # Getting coach's subdivision name
                    if i == 1:
                        coach_dict[coach_keys[i]] = get_subdivision_by_id(coach[i])['subdivision_name']
                    # Processing coach's info
                    elif i == 3:
                        coach_dict[coach_keys[i]] = [x.split('|') for x in coach[i][1:-1].split('][')]
                    else:
                        coach_dict[coach_keys[i]] = coach[i]
                coaches_arr.append(coach_dict)
            coaches = sorted(coaches_arr, key=lambda x: int(x['coach_id']))
        return coaches


# Getting coach by id
def get_coach_by_id(coach_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM coaches WHERE coach_id = {coach_id};""")
        coach = cursor.fetchone()
        if coach is not None:
            coach_keys = ['coach_id', 'coach_subdivision', 'coach_name', 'coach_info', 'coach_phone', 'coach_address']
            coach_dict = {}
            for i in range(len(coach_keys)):
                # Getting coach's subdivision name
                if i == 1:
                    coach_dict[coach_keys[i]] = get_subdivision_by_id(coach[i])['subdivision_name']
                # Processing coach's info
                elif i == 3:
                    coach_dict[coach_keys[i]] = [x.split('|') for x in coach[i][1:-1].split('][')]
                else:
                    coach_dict[coach_keys[i]] = coach[i]
            coach = coach_dict
        return coach


# Getting subdivision by id
def get_subdivision_by_id(subdivision_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM subdivisions WHERE subdivision_id = {subdivision_id};""")
        subdivision = cursor.fetchone()
        if subdivision is not None:
            subdivision_keys = ['subdivision_id', 'subdivision_name']
            subdivision_dict = {}
            for i in range(len(subdivision_keys)):
                subdivision_dict[subdivision_keys[i]] = subdivision[i]
            subdivision = subdivision_dict
        return subdivision


# Getting subdivision's id
def get_subdivision_id(subdivision_name):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT subdivision_id FROM subdivisions WHERE subdivision_name = '{subdivision_name}';""")
        subdivision = cursor.fetchone()
        if subdivision is not None:
            subdivision = subdivision[0]
        return subdivision


# Getting all schedules
def get_schedules():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM schedules;""")
        schedules = cursor.fetchall()
        if schedules is not None:
            schedules_arr = []
            schedules = sorted(schedules, key=lambda x: x[-1])
            # Processing correct schedules' positions
            if schedules[0][-1] != 1:
                update_schedule_position(schedules[0][0], 1)
                cursor.execute(f"""SELECT * FROM schedules;""")
                schedules = cursor.fetchall()
            for i in range(1, len(schedules)):
                if schedules[i][-1] != schedules[i - 1][-1] + 1:
                    update_schedule_position(schedules[i][0], schedules[i - 1][-1] + 1)
                    cursor.execute(f"""SELECT * FROM schedules;""")
                    schedules = cursor.fetchall()
            for schedule in schedules:
                schedule_keys = ['schedule_id', 'schedule_position']
                schedule_dict = {}
                for i in range(len(schedule_keys)):
                    schedule_dict[schedule_keys[i]] = schedule[i]
                schedules_arr.append(schedule_dict)
            schedules = schedules_arr
        return schedules


# Getting all news
def get_news():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM news;""")
        news = cursor.fetchall()
        if news is not None:
            news_arr = []
            for x in news:
                x_keys = ['news_id', 'news_date', 'news_title', 'news_text']
                x_dict = {}
                for i in range(len(x_keys)):
                    x_dict[x_keys[i]] = x[i]
                x_dict['news_date'] = datetime.datetime.strptime(x_dict['news_date'], '%d-%m-%Y %H:%M').strftime('%d-%m-%Y %H:%M')
                news_arr.append(x_dict)
            news = sorted(news_arr, key=lambda x: x['news_date'], reverse=True)
        return news


# Getting news by its news_id
def get_news_by_id(news_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM news WHERE news_id = {news_id};""")
        news = cursor.fetchone()
        if news is not None:
            news_keys = ['news_id', 'news_date', 'news_title', 'news_text']
            news_dict = {}
            for i in range(len(news_keys)):
                news_dict[news_keys[i]] = news[i]
            news = news_dict
        return news
