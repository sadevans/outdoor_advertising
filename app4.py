import json

from flask import Flask, render_template, redirect, session, url_for
from auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from blueprint_insert.route import blueprint_insert
from blueprint_schedule.route import blueprint_schedule
from basket.route import blueprint_order
from access import login_required, group_required


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/quaries')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.register_blueprint(blueprint_insert, url_prefix='/insert_data')
app.register_blueprint(blueprint_schedule, url_prefix='/schedule')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    if 'user_id' in session:
        if session.get('user_group') == None or session.get('user_group') == "external":
            session['user_group'] = "external"
            return render_template('external_user_menu.html')
        else:
            return render_template('internal_user_menu.html')
    else:
        return redirect(url_for('blueprint_auth.start_auth'))


@app.route('/exit')
def exit_func():
    if 'user_id' in session:
        session.clear()
    return 'Работа в системе завершена'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)