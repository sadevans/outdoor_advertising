import os.path

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


#меню запросов
@blueprint_query.route('/choose_quaries', methods=['GET', 'POST'])
@group_required
def choose_queries():
    return render_template('query_menu.html')


#запрос 1: показать все сведения об арендаторах, заключивших договора в х-месяце нннн-го года
@blueprint_query.route('/info_renters', methods=['GET', 'POST'])
@group_required
def info_renters():
    columns = ['Номер арендатора', 'Фамилия', 'Адрес', 'Номер телефона', 'Сфера деятельности', 'Дата заключения договора']
    if request.method == 'GET':
        return render_template('info_renters.html')
    else:
        date = request.form.get('input_date').split("-")
        print('date:', date)
        input_year = date[0]
        input_month = date[1]
        if input_month:
            _sql = provider.get('info_renters.sql', input_month=input_month, input_year = input_year)
            checking, schema = select(current_app.config['db_config'], _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(checking) == 0:
                message = 'Нет данных в базе данных для выполнения запроса'
                return render_template('message_query.html', message=message)
            else:
                return render_template('db_result.html', schema=columns, result=product_result)
        else:
            return "Повторите ввод"


#запрос 2: Показать, на какую сумму оформил заказов каждый арендатор в хххх году
@blueprint_query.route('/sum_order_renter', methods=['GET', 'POST'])
@group_required
def sum_order_renter():
    columns = ['Номер арендатора', 'Сумма заказов за указанный год']
    if request.method == 'GET':
        return render_template('sum_order_renter.html')
    else:
        input_year = int(request.form.get('input_year'))
        if input_year:
            _sql = provider.get('sum_order_renter.sql', input_year = input_year)
            checking, schema = select(current_app.config['db_config'], _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(checking) == 0:
                message = 'Нет данных в базе данных для выполнения запроса'
                return render_template('message_query.html', message=message)
            else:
                return render_template('db_result.html', schema=columns, result=product_result)
        else:
            return "Повторите ввод"


#запрос 3: Покажите номера билбордов, которые арендатор по фамилии ХХХ арендовал в х месяце хххх года.
@blueprint_query.route('/num_billb', methods=['GET', 'POST'])
@group_required
def num_billb():
    columns = ['Номер билборда']
    if request.method == 'GET':
        return render_template('num_billb.html')
    else:
        input_date = request.form.get('input_date').split("-")
        input_year = input_date[0]
        input_month = input_date[1]
        input_surname = request.form.get('input_surname')
        if input_year:
            _sql = provider.get('num_billb.sql', input_month = input_month, input_year = input_year, input_surname = input_surname)
            checking, schema = select(current_app.config['db_config'], _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(checking) == 0:
                message = 'Нет данных в базе данных для выполнения запроса'
                return render_template('message_query.html', message=message)
            else:
                return render_template('db_result.html', schema=columns, result=product_result)
        else:
            return "Повторите ввод"


@blueprint_query.route('/view_billboard_by_quality', methods=['GET', 'POST'])
@group_required
def view_billboard_by_quality():
    columns = ['Номер билборда', 'Размер билборда', 'Направление', 'Адрес установки', 'Стоимость аренды руб/мес']
    if request.method == 'GET':
        return render_template('view_billboard_by_quality.html')
    else:
        input_quality = int(request.form.get('input_quality'))
        if input_quality:
            _sql = provider.get('view_billboard_by_quality.sql', input_quality=input_quality)
            checking, schema = select(current_app.config['db_config'], _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(checking) == 0:
                message = 'Нет данных в базе данных для выполнения запроса'
                return render_template('message_query.html', message=message)
            else:
                return render_template('view_billboard_by_quality_result.html', schema=columns, result=product_result, input_quality=input_quality)
        else:
            return "Повторите ввод"


@blueprint_query.route('/view_billboard_by_direction', methods=['GET', 'POST'])
@group_required
def view_billboard_by_direction():
    columns = ['Номер билборда', 'Размер билборда', 'Адрес установки', 'Индекс качества', 'Стоимость аренды руб/мес']
    if request.method == 'GET':
        return render_template('view_billboard_by_direction.html')
    else:
        input_direction = request.form.get('input_direction')
        if input_direction:
            _sql = provider.get('view_billboard_by_direction.sql', input_direction=input_direction)
            checking, schema = select(current_app.config['db_config'], _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(checking) == 0:
                message = 'Нет данных в базе данных для выполнения запроса'
                return render_template('message_query.html', message=message)
            else:
                return render_template('view_billboard_by_direction_result.html', schema=columns, result=product_result, input_direction=input_direction)
        else:
            return "Повторите ввод"


# @blueprint_query.route('/view_schedule', methods=['GET', 'POST'])
# @group_required
# def view_schedule():
#     columns = ['Месяц начала аренды', 'Год начала аренды', 'Месяц конца аренды', 'Год конца аренды', 'Номер билборда']
#     if request.method == 'GET':
#         print('я тут нахуй')
#         _sql = provider.get('view_schedule.sql')
#         product_result, schema = select(current_app.config['db_config'], _sql)
#         return render_template('view_schedule.html', schema=columns, result=product_result)
#     else:
#         print('я тут блять')
#         input_direction = request.form.get('input_direction')
#         if input_direction:
#             _sql = provider.get('view_schedule.sql')
#             checking, schema = select(current_app.config['db_config'], _sql)
#             product_result, schema = select(current_app.config['db_config'], _sql)
#             if len(checking) == 0:
#                 message = 'Нет данных в базе данных для выполнения запроса'
#                 return render_template('message_query.html', message=message)
#             else:
#                 return render_template('view_schedule.html', schema=columns, result=product_result)
#         else:
#             return "Повторите ввод"