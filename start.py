from flask import Flask, request, redirect, flash, url_for, session, render_template

from modules.check import *
from modules.prepod import Prepod
from modules.slushatel import Slushatel

app = Flask(__name__)
app.secret_key = 'secret_key'

# Визуализация формы входа
@app.route('/')
def index():
    return render_template('login.html')

# Обработка формы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if  request.method == 'POST':

        check = check_login(request.form)
        if check == False:
            flash("Введите корректные данные!")
            return redirect(url_for('index'))
        
        session['auth'] = True
        session['user'] = request.form['login']
        session['type'] = check

        if check == 'Преподаватель':
            return redirect(url_for('prepod'))
        else :
            return redirect(url_for('slushatel'))

    if 'auth' not in session:
        return redirect(url_for('index'))
    
# Визуализация формы регистрации
@app.route('/reg')
def reg():
    return render_template('register.html')

# BackEnd формы визуализации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        check = check_register(request.form)
        if not check:
            flash('Пользователь с такими логином уже существует')
            return redirect(url_for('reg'))

        flash('Вы успешно зарегестрированы в системе. Теперь можете войти с используя свои данные')
        return redirect(url_for('index'))

    return redirect(url_for('reg'))

# Визуализация основной страницы преподавателя 
@app.route('/prepod')
def prepod():
    if 'auth' not in session:
        session.clear()
        return redirect(url_for('index'))

    prepod = Prepod(session['user'])
    return render_template('prepod.html', name=prepod.name, data=prepod.get_query_data())
    
# Обработка запросов со стороны преподавателя
@app.route('/prepod_api', methods=['GET', 'POST'])
def prepod_api():
    if 'action' in request.form:
        prepod = Prepod(session['user'])
        action = request.form['action']

        if action == 'update_status':
            prepod.update_status(request.form['index'], request.form['status'])
        if action == 'update_index':
            prepod.update_index(int(request.form['old']), int(request.form['new']))
        if action == 'Выйти':
            session.clear()
            return redirect(url_for('index'))
        if action in ['Принять', 'Удалить']:
            prepod.drop_index(int(request.form['id']))


    return redirect(url_for('prepod'))

# Визуализация основной страницы слушатля 
@app.route('/slushatel')
def slushatel():
    if 'auth' not in session:
        session.clear()
        return redirect(url_for('index'))

    slushatel = Slushatel(session['user'])
    return render_template(
        'slushatel.html', 
        name=slushatel.fullname, 
        data=slushatel.get_queue_data(),
        prepod_names=Prepod.get_prepods_name())

# Обработка запросов со стороны слушателя
@app.route('/slushatel_api', methods=['GET', 'POST'])
def slushatel_api():
    if 'action' in request.form:
        slushatel = Slushatel(session['user'])
        action = request.form['action']

        if action == 'Выйти':
            session.clear()
            return redirect(url_for('index'))

        if action == 'Встать в очередь':
            slushatel.get_in_line(request.form['prepod_name'])

    return redirect(url_for('slushatel'))

if __name__ == '__main__':
    app.run()