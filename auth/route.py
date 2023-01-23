from flask import Blueprint, request, render_template, current_app, session, redirect, url_for
from db_work import select_dict, save_order_with_list
from sql_provider import SQLProvider
import os
from typing import Optional, Dict


blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_auth.route('/', methods = ['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)

            if user_info:
                user_dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                print('user id:', session.get('user_id'))
                session['user_group'] = user_dict['user_group']
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Повторите ввод')


def define_user(login: str, password: str) -> Optional[Dict]: #Проверка соответсвия пароля/логина
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    user_info = None

    for sql_search in [sql_internal, sql_external]:
        user_info = select_dict(current_app.config['db_config'], sql_search)
        if user_info:
            break
    return user_info