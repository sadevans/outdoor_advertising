import os.path
from flask import *
from db_work import select, call_proc
from access import *
from sql_provider import SQLProvider


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


report_list = [
    {'rep_name':'Отчет о суммарной длительности аренды билбордов за год ', 'rep_id':'1'},
    {'rep_name':'Отчет о суммарной стоимости всех заказов, оформленных за год', 'rep_id':'2'}#,
    # {'rep_name':'Отчет о сумме заказов по направлениям за год', 'rep_id':'3'}
]


report_url = {
    '1': {'create_rep':'bp_report.create_rep1', 'view_rep':'bp_report.view_rep1'},
    '2': {'create_rep':'bp_report.create_rep2', 'view_rep':'bp_report.view_rep2'}#,
    # '3': {'create_rep':'bp_report.create_rep3', 'view_rep':'bp_report.view_rep3'}
}


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id = ', rep_id)
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep = ', url_rep)
        return redirect(url_for(url_rep))
    # из формы получает номер отчета и какую кнопку


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        print("POST_create")
        rep_year = int(request.form.get('input_year'))
        if rep_year:
            _sql_check = provider.get('rep1.sql', in_year=rep_year)
            checking, schema = select(current_app.config['db_config'], _sql_check)
            if len(checking) == 0:
                res = call_proc(current_app.config['db_config'], 'year_report', rep_year)
                print('res=', res)
                _sql_check1 = provider.get('rep1.sql', in_year=rep_year)
                checking, schema = select(current_app.config['db_config'], _sql_check1)
                if len(checking) == 0:
                    message='Нет данных в базе данных для создания отчета'
                    return render_template('message.html', message=message)
                else:
                    message='Отчет создан'
                    return render_template('message.html', message=message)
            else:
                message='Такой отчет уже существует'
                return render_template('message.html', message=message)
        else:
            message = 'Повторите ввод'
            return render_template('message.html', message=message)


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    columns = ['Номер билборда', 'Адрес установки', 'Общее количество месяцев аренды']
    if request.method == 'GET':
        return render_template('view_rep.html')
    else:
        rep_year = int(request.form.get('input_year'))
        print(rep_year)
        if rep_year:
            _sql = provider.get('rep1.sql', in_year=rep_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                message = 'Нет данных в базе данных для просмотра отчета'
                return render_template('message.html', message=message)
            else:
                return render_template('result_year_rep.html', schema=columns, result=product_result, rep_year=rep_year)
        else:
            message = 'Повторите ввод'
            return render_template('message.html', message=message)


@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        print("GET_create")
        return render_template('create_rep2.html')
    else:
        print("POST_create")
        rep_year = int(request.form.get('input_year'))
        if rep_year:
            _sql_check = provider.get('rep2.sql', in_year=rep_year)
            checking, schema = select(current_app.config['db_config'], _sql_check)
            if len(checking) == 0:
                res = call_proc(current_app.config['db_config'], 'sum_orderings_year_report', rep_year)
                print('res=', res)
                _sql_check1 = provider.get('rep1.sql', in_year=rep_year)
                checking, schema = select(current_app.config['db_config'], _sql_check1)
                if len(checking) == 0:
                    message = 'Нет данных в базе данных для создания отчета'
                    return render_template('message.html', message=message)
                else:
                    message = 'Отчет создан'
                    return render_template('message.html', message=message)
            else:
                message='Такой отчет уже существует'
                return render_template('message.html', message=message)
        else:
            message = 'Повторите ввод'
            return render_template('message.html', message=message)


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    columns = ['Общее количество заказов за указанный год', 'Общая сумма заказов за указанный год']
    if request.method == 'GET':
        return render_template('view_rep2.html')
    else:
        rep_year = int(request.form.get('input_year'))
        print(rep_year)
        if rep_year:
            _sql = provider.get('rep2.sql', in_year=rep_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                message = 'Нет данных в базе данных для просмотра отчета'
                return render_template('message.html', message=message)
            else:
                return render_template('result_year_rep.html', schema=columns, result=product_result, rep_year=rep_year)
        else:
            message = 'Повторите ввод'
            return render_template('message.html', message=message)


# @blueprint_report.route('/create_rep3', methods=['GET', 'POST'])
# @group_required
# def create_rep3():
#     message='Создание данного отчета пока невозможно'
#     return render_template('message.html', message=message)
#
#
# @blueprint_report.route('/view_rep3', methods=['GET', 'POST'])
# @group_required
# def view_rep3():
#     message = 'Просмотр данного отчета пока невозможен'
#     return render_template('message.html', message=message)


# @blueprint_report.route('/create_rep3', methods=['GET', 'POST'])
# @group_required
# def create_rep3():
#     if request.method == 'GET':
#         print("GET_create")
#         return render_template('create_rep2.html')
#     else:
#         print("POST_create")
#         rep_year = request.form.get('input_year')
#         if rep_year:
#             _sql_check = provider.get('rep2.sql', in_year=rep_year)
#             checking, schema = select(current_app.config['db_config'], _sql_check)
#             if len(checking) == 0:
#                 _sql = provider.get('insert_direction_year_report.sql', in_year=rep_year)
#                 res = call_proc(current_app.config['db_config'], 'directions_report', rep_year)
#                 print('res=', res)
#                 message='Отчет создан'
#                 return render_template('message.html', message=message)
#             else:
#                 message='Такой отчет уже существует'
#                 return render_template('message.html', message=message)
#         else:
#             return "Повторите ввод"
#
#
# @blueprint_report.route('/view_rep3', methods=['GET', 'POST'])
# @group_required
# def view_rep3():
#     columns = ['Общее количество заказов за указанный год', 'Общая сумма заказов за указанный год']
#     if request.method == 'GET':
#         return render_template('view_rep2.html')
#     else:
#         rep_year = request.form.get('input_year')
#         print(rep_year)
#         if rep_year:
#             _sql = provider.get('rep2.sql', in_year=rep_year)
#             product_result, schema = select(current_app.config['db_config'], _sql)
#             return render_template('result_year_rep.html', schema = columns, result = product_result, rep_year=rep_year)
#         else:
#             return "Повторите ввод"


# @blueprint_report.route('/create_rep1')
# def create_rep1():
#     rep_month = 9       #заглушка, тут данные должны считыватья из формы ввода
#     rep_year = 2022
#     res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year)
#     print('res = ', res)
#     return render_template('report_created.html')


# @blueprint_report.route('/page1')
# @group_required
# def report_page1():
#     return render_template('page1.html')
#
#
# @blueprint_report.route('/page2.html')
# @group_required
# def report_page2():
#     return render_template('page2.html')