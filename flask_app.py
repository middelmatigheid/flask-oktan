import os
import pandas as pd
import datetime
from flask import Flask, redirect, url_for, render_template, request, send_file, session
import database as db

# Initializing flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)


# Main page
@app.route('/')
def home():
    return render_template('main.html')


# Services and prices page
@app.route('/services-and-prices/')
def services_and_prices():
    # Checking excel file's format
    fileformat = 'xlsx'
    if os.path.exists(f"static/excel/services-and-prices.xls"):
        fileformat = 'xls'

    # Getting excel file's sheet names
    sheet_names = pd.ExcelFile(f'static/excel/services-and-prices.{fileformat}').sheet_names
    # Transforming excel file to a valid format
    tables = []
    tables_names = {}

    # Setting headers of the tables
    if 'ЗАГОЛОВКИ' in sheet_names:
        excel = pd.read_excel(f'static/excel/services-and-prices.{fileformat}', sheet_name='ЗАГОЛОВКИ')
        for i in range(excel.shape[0]):
            tables_names[str(list(excel.iloc[i])[0])] = str(list(excel.iloc[i])[1])
    else:
        for x in sheet_names:
            tables_names[x] = x

    # Processing excel file's lists
    for i in range(len(sheet_names)):
        excel = pd.read_excel(f'static/excel/services-and-prices.{fileformat}', sheet_name=i).fillna('NaN')
        if sheet_names[i] != 'ЗАГОЛОВКИ':
            table = []
            res = []

            # Processing column names
            for x in list(excel.columns):
                # Checking if cells are merged
                if x.split()[0] == 'Unnamed:' and len(res) != 0:
                    res[-1][0] += 1
                # Checking empty cell
                elif x != '---':
                    res.append([1, str(x)])
                else:
                    res.append([1, ''])
            table.append(res)

            # Processing rest of the list
            for j in range(excel.shape[0]):
                res = []
                for x in list(excel.iloc[j]):
                    # Checking if cells are merged
                    if x == 'NaN' and len(res) != 0:
                        res[-1][0] += 1
                    # Checking empty cell
                    elif x != '---':
                        res.append([1, str(x)])
                    else:
                        res.append([1, ''])
                table.append(res)
            tables.append([tables_names[sheet_names[i]], table])

    return render_template('services-and-prices.html', tables=tables)


# Downloading excel files
@app.route('/download/<file>')
def download(file):
    if 'admin' not in session:
        return redirect(url_for('home'))
    if os.path.exists(f"static/excel/{file}.xls"):
        return send_file(f'static/excel/{file}.xls', as_attachment=True, download_name=f'{file}.xls')
    else:
        return send_file(f'static/excel/{file}.xlsx', as_attachment=True, download_name=f'{file}.xlsx')


# Services and prices admin page
@app.route('/services-and-prices-admin/', methods=['POST', 'GET'])
def services_and_prices_admin():
    if 'admin' not in session:
        return redirect(url_for('home'))
    # Processing POST request
    if request.method == 'POST':
        file = request.files['excel']
        if file and file.filename.split('.')[-1] in ['xlsx', 'xls']:
            # Deleting previous excel file
            if os.path.exists(f"static/excel/services-and-prices.xlsx"):
                os.remove(f"static/excel/services-and-prices.xlsx")
            if os.path.exists(f"static/excel/services-and-prices.xls"):
                os.remove(f"static/excel/services-and-prices.xls")
            # Saving new excel file
            db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} UPDATED SERVICES AND PRICES EXCEL FILE")
            file.save(f"static/excel/services-and-prices.{file.filename.split('.')[-1]}")
        return redirect(url_for('services_and_prices_admin'))

    # Processing GET request
    else:
        # Checking excel file's format
        fileformat = 'xlsx'
        if os.path.exists(f"static/excel/services-and-prices.xls"):
            fileformat = 'xls'

        # Getting excel file's sheet names
        sheet_names = pd.ExcelFile(f'static/excel/services-and-prices.{fileformat}').sheet_names
        # Transforming excel file to a valid format
        tables = []
        tables_names = {}

        # Setting headers of the tables
        if 'ЗАГОЛОВКИ' in sheet_names:
            excel = pd.read_excel(f'static/excel/services-and-prices.{fileformat}', sheet_name='ЗАГОЛОВКИ')
            for i in range(excel.shape[0]):
                tables_names[str(list(excel.iloc[i])[0])] = str(list(excel.iloc[i])[1])
        else:
            for x in sheet_names:
                tables_names[x] = x

        # Processing excel file's lists
        for i in range(len(sheet_names)):
            excel = pd.read_excel(f'static/excel/services-and-prices.{fileformat}', sheet_name=i).fillna('NaN')
            if sheet_names[i] != 'ЗАГОЛОВКИ':
                table = []
                res = []

                # Processing column names
                for x in list(excel.columns):
                    # Checking if cells are merged
                    if x.split()[0] == 'Unnamed:' and len(res) != 0:
                        res[-1][0] += 1
                    # Checking empty cell
                    elif x != '---':
                        res.append([1, str(x)])
                    else:
                        res.append([1, ''])
                table.append(res)

                # Processing rest of the list
                for j in range(excel.shape[0]):
                    res = []
                    for x in list(excel.iloc[j]):
                        # Checking if cells are merged
                        if x == 'NaN' and len(res) != 0:
                            res[-1][0] += 1
                        # Checking empty cell
                        elif x != '---':
                            res.append([1, str(x)])
                        else:
                            res.append([1, ''])
                    table.append(res)
                tables.append([tables_names[sheet_names[i]], table])

        return render_template('services-and-prices-admin.html', tables=tables)


# Coaches page
@app.route('/coaches/')
def coaches():
    return render_template('coaches.html')


# Coaches page
@app.route('/coaches-admin/')
def coaches_admin():
    if 'admin' not in session:
        return redirect(url_for('home'))
    return render_template('coaches-admin.html')


# Subdivision's coaches page
@app.route('/coaches-<subdivision>/', methods=['POST', 'GET'])
def coaches_subdivision(subdivision):
    # Processing POST request
    if request.method == 'POST':
        # Transforming request data to dictionary
        request_res = list(request.form.lists())
        request_dict = {}
        for x in request_res:
            request_dict[x[0]] = x[1]

        # Checking if coach is deleted
        if request_dict['coach_is_deleted'][0] == '1':
            # Deleting coach from database
            db.delete_coach(request_dict['coach_id'][0])
            # Deleting coach's image
            if os.path.exists(f"static/images/coaches/{request_dict['coach_id'][0]}.png"):
                os.remove(f"static/images/coaches/{request_dict['coach_id'][0]}.png")
            if os.path.exists(f"static/images/coaches/{request_dict['coach_id'][0]}.jpeg"):
                os.remove(f"static/images/coaches/{request_dict['coach_id'][0]}.jpeg")
            if os.path.exists(f"static/images/coaches/{request_dict['coach_id'][0]}.jpg"):
                os.remove(f"static/images/coaches/{request_dict['coach_id'][0]}.jpg")
        else:
            # Transforming coach's info to be valid for next operations
            coach_info = ''
            for x in filter(lambda y: y.split()[0] == 'coach_list_item', request_dict.keys()):
                coach_info += '[' + '|'.join(filter(lambda y: y != '', request_dict[x])) + ']'

            # Updating coach's info
            if db.get_coach_by_id(request_dict['coach_id'][0]) and db.get_subdivision_id(request_dict['coach_subdivision'][0]):
                # Saving coach's image
                file = request.files['coach_img']
                if file:
                    file.save(f"static/images/coaches/{int(request_dict['coach_id'][0])}.{file.filename.split('.')[-1]}")
                db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} UPDATED COACH {request_dict['coach_id'][0]}")
                db.update_coach(request_dict['coach_id'][0], db.get_subdivision_id(request_dict['coach_subdivision'][0]), request_dict['coach_name'][0], coach_info, request_dict['coach_phone'][0], request_dict['coach_address'][0])

            # Adding new coach to the database
            elif db.get_subdivision_id(request_dict['coach_subdivision'][0]):
                db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} ADDED NEW COACH {request_dict['coach_name'][0]}")
                coach_id = db.add_coach(db.get_subdivision_id(request_dict['coach_subdivision'][0]), request_dict['coach_name'][0], coach_info, request_dict['coach_phone'][0], request_dict['coach_address'][0])
                # Saving coach's image
                file = request.files['coach_img']
                if file:
                    file.save(f"static/images/coaches/{int(coach_id)}.{file.filename.split('.')[-1]}")

        return redirect(url_for('coaches_subdivision', subdivision=subdivision))

    # Processing GET request
    else:
        # Processing admin page
        if '-' in subdivision and subdivision.split('-')[1] == 'admin' and db.get_subdivision_id(subdivision.split('-')[0]):
            # Getting coaches' infos
            coaches_arr = db.get_coaches_by_subdivision(db.get_subdivision_id(subdivision.split('-')[0]))
            for coach in coaches_arr:
                # Checking coach's image format
                if os.path.exists(f"static/images/coaches/{coach['coach_id']}.png"):
                    coach['coach_img'] = "png"
                elif os.path.exists(f"static/images/coaches/{coach['coach_id']}.jpeg"):
                    coach['coach_img'] = "jpeg"
                elif os.path.exists(f"static/images/coaches/{coach['coach_id']}.jpg"):
                    coach['coach_img'] = "jpg"
                else:
                    coach['coach_img'] = 'None'
            return render_template('coaches-subdivision-admin.html', coaches=coaches_arr)

        elif db.get_subdivision_id(subdivision):
            # Getting coaches' infos
            coaches_arr = db.get_coaches_by_subdivision(db.get_subdivision_id(subdivision))
            for coach in coaches_arr:
                # Checking coach's image format
                if os.path.exists(f"static/images/coaches/{coach['coach_id']}.png"):
                    coach['coach_img'] = "png"
                elif os.path.exists(f"static/images/coaches/{coach['coach_id']}.jpeg"):
                    coach['coach_img'] = "jpeg"
                elif os.path.exists(f"static/images/coaches/{coach['coach_id']}.jpg"):
                    coach['coach_img'] = "jpg"
                else:
                    coach['coach_img'] = 'None'
            return render_template('coaches-subdivision.html', coaches=coaches_arr)

        else:
            return redirect(url_for('coaches'))


# Schedule page
@app.route('/schedule/')
def schedule():
    schedules_arr = db.get_schedules()
    schedules = []
    for schedule in schedules_arr:
        if os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.png"):
            schedule['schedule_img'] = "png"
            schedules.append(schedule)
        elif os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.jpeg"):
            schedule['schedule_img'] = "jpeg"
            schedules.append(schedule)
        elif os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.jpg"):
            schedule['schedule_img'] = "jpg"
            schedules.append(schedule)
        else:
            db.add_log('APP', datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"SCHEDULE {schedule['schedule_id']} WAS DELETED DUE TO IMAGE ABSENCE")
            db.delete_schedule(int(schedule['schedule_id']))
    return render_template('schedule.html', schedules=schedules)


# Schedule admin page
@app.route('/schedule-admin/', methods=['POST', 'GET'])
def schedule_admin():
    if 'admin' not in session:
        return redirect(url_for('home'))
    # Processing POST request
    if request.method == 'POST':
        # Transforming request data to dictionary
        request_res = list(request.form.lists())
        request_dict = {}
        for x in request_res:
            request_dict[x[0]] = x[1]

        # Processing schedules
        for i in range(len(request_dict['schedule_id'])):
            # Deleting schedule
            if request_dict['schedule_is_deleted'][i] == '1':
                db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} DELETED SCHEDULE {request_dict['schedule_id'][i]}")
                db.delete_schedule(int(request_dict['schedule_id'][i]))
            # Updating schedule
            elif request_dict['schedule_id'][i] != '-1':
                db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} UPDATED SCHEDULE {request_dict['schedule_id'][i]}")
                db.update_schedule_position(int(request_dict['schedule_id'][i]), int(request_dict['schedule_position'][i]))

        # Adding a new schedule
        file = request.files['schedule_img']
        if file:
            schedule = db.add_schedule(int(request_dict['schedule_position'][-1]))
            file.save(f"static/images/schedules/{schedule}.{file.filename.split('.')[-1]}")

        return redirect(url_for('schedule_admin'))

    # Processing GET request
    else:
        schedules_arr = db.get_schedules()
        schedules = []
        for schedule in schedules_arr:
            if os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.png"):
                schedule['schedule_img'] = "png"
                schedules.append(schedule)
            elif os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.jpeg"):
                schedule['schedule_img'] = "jpeg"
                schedules.append(schedule)
            elif os.path.exists(f"static/images/schedules/{schedule['schedule_id']}.jpg"):
                schedule['schedule_img'] = "jpg"
                schedules.append(schedule)
            else:
                db.delete_schedule(int(schedule['schedule_id']))
        return render_template('schedule-admin.html', schedules=schedules)


# All news page
@app.route('/news')
def all_news():
    # Getting news
    news = db.get_news()[:10]
    # Checking news' image format
    for x in news:
        if os.path.exists(f"static/images/news/{x['news_id']}.png"):
            x['news_img'] = "png"
        elif os.path.exists(f"static/images/news/{x['news_id']}.jpeg"):
            x['news_img'] = "jpeg"
        elif os.path.exists(f"static/images/news/{x['news_id']}.jpg"):
            x['news_img'] = "jpg"
        else:
            x['news_img'] = "None"
    return render_template('all-news.html', news=news)


# Sending more news
@app.route('/news/add-posts-<page>')
def add_news(page):
    page = int(page)
    news = db.get_news()[(page - 1) * 10: page * 10]
    return [render_template('add-news.html', news=news), len(news) == 10]


# All news admin page
@app.route('/news-admin')
def all_news_admin():
    if 'admin' not in session:
        return redirect(url_for('home'))
    # Getting news
    news = db.get_news()[:10]
    # Checking news' image format
    for x in news:
        if os.path.exists(f"static/images/news/{x['news_id']}.png"):
            x['news_img'] = "png"
        elif os.path.exists(f"static/images/news/{x['news_id']}.jpeg"):
            x['news_img'] = "jpeg"
        elif os.path.exists(f"static/images/news/{x['news_id']}.jpg"):
            x['news_img'] = "jpg"
        else:
            x['news_img'] = "None"
    return render_template('all-news-admin.html', news=news)


# Sending more news
@app.route('/news-admin/add-posts-<page>')
def add_news_admin(page):
    if 'admin' not in session:
        return redirect(url_for('home'))
    page = int(page)
    news = db.get_news()[(page - 1) * 10: page * 10]
    return [render_template('add-news-admin.html', news=news), len(news) == 10]


# Certain news page
@app.route('/news/<news_id>')
def news(news_id):
    # Getting news
    news = db.get_news_by_id(int(news_id))
    # Checking news' image format
    if os.path.exists(f"static/images/news/{news['news_id']}.png"):
        news['news_img'] = "png"
    elif os.path.exists(f"static/images/news/{news['news_id']}.jpeg"):
        news['news_img'] = "jpeg"
    elif os.path.exists(f"static/images/news/{news['news_id']}.jpg"):
        news['news_img'] = "jpg"
    else:
        news['news_img'] = "None"
    return render_template('news.html', news=news)


# Certain news admin page
@app.route('/news-admin/<news_id>', methods=['POST', 'GET'])
def news_admin(news_id):
    if 'admin' not in session:
        return redirect(url_for('home'))
    # Processing POST request
    if request.method == 'POST':
        # Transforming request data to dictionary
        request_res = list(request.form.lists())
        request_dict = {}
        for x in request_res:
            request_dict[x[0]] = x[1][0]

        # Checking if the news is new
        if news_id == '-1':
            news_id = db.add_news(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), request_dict['news_title'], request_dict['news_text'])
            db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
                       f"ADMIN {request.remote_addr} {session['admin']} ADDED NEW NEWS {request_dict['news_title']}")
            file = request.files['news_img']
            if file:
                file.save(f"static/images/news/{news_id}.{file.filename.split('.')[-1]}")
        # Updating existing news
        else:
            db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} UPDATED NEWS {db.get_news_by_id(int(request_dict['news_id']))}")
            db.update_news(int(request_dict['news_id']), request_dict['news_title'], request_dict['news_text'])
            file = request.files['news_img']
            if file:
                if os.path.exists(f"static/images/news/{request_dict['news_id'][0]}.png"):
                    os.remove(f"static/images/news/{request_dict['news_id'][0]}.png")
                if os.path.exists(f"static/images/news/{request_dict['news_id'][0]}.jpeg"):
                    os.remove(f"static/images/news/{request_dict['news_id'][0]}.jpeg")
                if os.path.exists(f"static/images/news/{request_dict['news_id'][0]}.jpg"):
                    os.remove(f"static/images/news/{request_dict['news_id'][0]}.jpg")
                file.save(f"static/images/news/{news_id}.{file.filename.split('.')[-1]}")

        return redirect(url_for('news_admin', news_id=news_id))
    # Processing GET method
    else:
        # Checking if the news is new
        if news_id == '-1':
            news = {}
            news_keys = ['news_id', 'news_date', 'news_title', 'news_text', 'news_img']
            news_values = ['-1', '01.01.2001', 'Заголовок', 'Текст новости', 'None']
            for i in range(len(news_keys)):
                news[news_keys[i]] = news_values[i]
        # Viewing existing news
        else:
            news = db.get_news_by_id(int(news_id))
            if os.path.exists(f"static/images/news/{news['news_id']}.png"):
                news['news_img'] = "png"
            elif os.path.exists(f"static/images/news/{news['news_id']}.jpeg"):
                news['news_img'] = "jpeg"
            elif os.path.exists(f"static/images/news/{news['news_id']}.jpg"):
                news['news_img'] = "jpg"
            else:
                news['news_img'] = "None"
        return render_template('news-admin.html', news=news)


# Deleting news
@app.route('/news-admin/delete/<news_id>')
def news_delete(news_id):
    if 'admin' not in session:
        return redirect(url_for('home'))
    db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} DELETED NEWS {db.get_news_by_id(int(news_id))['news_title']}")
    db.delete_news(int(news_id))
    return redirect(url_for('all_news_admin'))


# Admin page
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    # Processing POST request
    if request.method == 'POST':
        # Transforming request data to dictionary
        request_res = list(request.form.lists())
        request_dict = {}
        for x in request_res:
            request_dict[x[0]] = x[1][0]

        # Checking if adding a new admin
        if request_dict['admin_new'] == '1':
            flag = False
            if db.get_admin_by_login(request_dict['form_login']) is not None:
                flag = True
            else:
                db.add_admin(request_dict['form_login'], request_dict['form_password'])
            return render_template('admin.html', admins=db.get_admins(), logs=db.get_logs()[:10], flag=flag)
        # Logging to the admin page
        else:
            if db.get_admin_by_login(request_dict['form_login'])['admin_password'] == request_dict['form_password']:
                session.permanent = False
                session['admin'] = request_dict['form_login']
                db.add_log(request_dict['form_login'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {request_dict['form_login']} LOGGED IN")
                return render_template('admin.html', admins=db.get_admins(), logs=db.get_logs()[:10], flag=False)

            return render_template('login.html')

    # Processing GET request
    else:
        if 'admin' in session:
            return render_template('admin.html', admins=db.get_admins(), logs=db.get_logs()[:10], flag=False)
        else:
            return render_template('login.html')


# Adding more logs
@app.route('/admin/add-logs-<page>')
def add_logs_admin(page):
    if 'admin' not in session:
        return redirect(url_for('home'))
    page = int(page)
    logs = db.get_logs()[(page - 1) * 10: page * 10]
    return [render_template('add-logs.html', logs=logs), len(logs) == 10]


# Deleting admin
@app.route('/admin/delete/<admin_login>')
def admin_delete(admin_login):
    if 'admin' not in session:
        return redirect(url_for('home'))
    db.delete_admin(admin_login)
    db.add_log(session['admin'], datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), f"ADMIN {request.remote_addr} {session['admin']} DELETED ADMIN {admin_login}")
    return redirect(url_for('admin'))


# On startup function adding main coaches' data to the database
def start():
    db.delete_tables()
    db.create_tables()

    # Adding subdivisions
    db.add_subdivision('delphin')
    db.add_subdivision('oktan')
    db.add_subdivision('olimp')
    db.add_subdivision('tonus')
    db.add_subdivision('vodolei')
    db.add_subdivision('zhemchuzhina')

    # Adding delphin's coaches
    subdivision = '1'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding oktan's coaches
    subdivision = '2'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding olimp's coaches
    subdivision = '3'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding tonus' coaches
    subdivision = '4'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding vodolei's coaches
    subdivision = '5'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding zhemchuzhina's coaches
    subdivision = '6'
    name = 'Имя тренера — специализация тренера'
    info = '[<Достижения>|достижение][<Направления работы>|направление работы]'
    phone = '+8 888 888 88 88'
    address = 'Москва'
    db.add_coach(subdivision, name, info, phone, address)

    # Adding schedules
    db.add_schedule(1)
    db.add_schedule(2)
    db.add_schedule(3)
    db.add_schedule(4)
    db.add_schedule(5)
    db.add_schedule(6)
    db.add_schedule(7)
    db.add_schedule(8)

    # Adding news
    for i in range(11):
        db.add_news('01-01-2001 01:01', 'Название новости', 'Текст новости')

    # Adding admin
    db.add_admin('Логин', 'Пароль')


# Starting the app
if __name__ == '__main__':
    #start()
    app.run(debug=True)
