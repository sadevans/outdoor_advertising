import os.path

from flask import *
from db_work import *
from sql_provider import SQLProvider
from db_context_manager import DBConnection
from access import *

temp = 0
blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
_sql = []


@blueprint_order.route('/order_index', methods=['GET', 'POST'])
@group_required
def order_index():
    print(session)
    summary = 0
    db_config = current_app.config['db_config']
    global temp
    if temp == 0:
        if request.method == 'GET':
            return render_template('basket_properties.html')
        else:
            global _sql
            print('user1 id:', session.get('user_id'))
            input_date1 = request.form.get("input_date1").split("-")
            input_date2 = request.form.get("input_date2").split("-")
            year_b = int(input_date1[0])
            month_b = int(input_date1[1])
            print('year_b type, month_b type', type(year_b), type(month_b))
            year_e = int(input_date2[0])
            month_e = int(input_date2[1])
            city = request.form.get("input_city")
            direction = request.form.get("input_direction")
            if len(city) != 0 and len(direction) != 0:
                _sql = provider.get('get_bill_by_date_city_dir.sql', month_b=month_b, year_b=year_b, month_e=month_e,
                                    year_e=year_e, city=city, direction=direction)

            if len(city) == 0 and len(direction) != 0:
                _sql = provider.get('get_bill_by_date_dir.sql', month_b=month_b, year_b=year_b, month_e=month_e,
                                    year_e=year_e, direction=direction)
            else:
                _sql = provider.get('get_bill_by_date_city.sql', month_b=month_b, year_b=year_b,
                                    month_e=month_e, year_e=year_e, city=city)
            if len(city) == 0 and len(direction) == 0:
                _sql = provider.get('get_bill_by_date.sql', month_b=month_b, year_b=year_b,
                                    month_e=month_e, year_e=year_e)
            temp = 1
            return redirect(url_for('bp_order.order_index'))
    else:
        if request.method == 'GET':
            items = select_dict(db_config, _sql)
            basket_items = session.get('basket', {})
            print('items', items)
            for i in basket_items:
                summary = summary + int(basket_items[i]['duration'])*int(basket_items[i]['cost'])
            session['sum'] = summary
            return render_template('basket_order.html', items=items, basket=basket_items, sum=summary)
        else:
            bil_id = request.form['id_billboard']
            # print('bil id:', bil_id)
            sql = provider.get('select_item.sql', id_billboard=bil_id)
            items = select_dict(db_config, sql)
            date_order = request.form['date_order'].split("-")
            year = int(date_order[0])
            month = int(date_order[1])
            duration = int(request.form['duration'])
            add_to_basket(bil_id, items, year, month, duration)
            return redirect(url_for('bp_order.order_index'))


def check(bil_id, year, month, duration):
    month_end = month + duration
    year_end = year
    if int(month_end) > 12:
        year_end = year + int(month_end / 12)
        month_end = int(month_end) % 12
        _sql_check = provider.get('check.sql', bil_id=bil_id, month_b=month, year_b=year, month_e=month_end,
                                  year_e=year_end)
        checking, schema = select(current_app.config['db_config'], _sql_check)
        return len(checking)


def add_to_basket(prod_id: str, items: dict, year, month, duration):
    curr_basket = session.get('basket', {})
    if check(prod_id, year, month, duration) == 0:
        message = 'Введите другую длительность аренды'
        return render_template('message_basket.html', message=message)
    else:
        curr_basket[prod_id] = {
        'id_billboard': items[0]['id_billboard'],
        'address': items[0]['address'],
        'direction': items[0]['direction'],
        'cost': items[0]['cost'],
        'year_order': year,
        'month_order': month,
        'duration': duration
    }
    print('items:', items)
    session['basket'] = curr_basket
    session.permanent = True
    return True


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
@group_required
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket, provider)
    print('user id:', user_id)
    if order_id:
        call_proc(current_app.config['db_config'], 'add_schedule_lines', order_id)
        session.pop('basket')
        message = 'Заказ создан'
        return render_template('message_basket.html', message=message)
        # return render_template('order_created.html', order_id=order_id)
    else:
        message = 'Что-то пошло не так'
        return render_template('message_basket.html', message=message)


# def save_order_with_list(dbconfig: dict, user_id: int, current_basket):
#     with DBConnection(dbconfig) as cursor:
#         if cursor is None:
#             raise ValueError('Cursor not created')
#         print("created")
#         print(user_id)
#         summ = session.get('sum')
#         _sql1 = provider.get('insert_order.sql', user_id=user_id, tot_cost=summ)
#         result1 = cursor.execute(_sql1)
#         if result1 == 1:
#             _sql2 = provider.get('select_order_id.sql', user_id=user_id)
#             cursor.execute(_sql2)
#             order_id = cursor.fetchall()[0][0]
#             print('order_id= ', order_id)
#             if order_id:
#                 for key in current_basket:
#                     print(current_basket[key])
#                     month_beg = int(current_basket[key]['month_order'])
#                     print('month beg type:', type(month_beg))
#                     year_beg = int(current_basket[key]['year_order'])
#                     duration = int(current_basket[key]['duration'])
#                     print('duration type:', type(duration))
#                     cost = current_basket[key]['cost']
#                     month_end = month_beg + duration
#                     year_end = year_beg
#                     if int(month_end) > 12:
#                         year_end = year_beg + int(month_end / 12)
#                         month_end = int(month_end) % 12
#                         print('month end type:', type(month_end))
#                     _sql3 = provider.get('insert_order_list.sql', id_ordering=order_id, id_billboard=key,
#                                          month_beg=month_beg, year_beg=year_beg, duration=duration,
#                                          month_end=month_end, year_end=year_end, cost=cost)
#                     print(_sql3)
#                     print('basket:', current_basket)
#                     cursor.execute(_sql3)
#                 return order_id


@blueprint_order.route('/clear_basket')
@group_required
def clear_basket():
    print(session)
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))