# import os.path
from typing import Tuple, List
from db_context_manager import DBConnection
# from sql_provider import SQLProvider
from flask import *


# provider = SQLProvider(os.path.join(os.path.dirname('C:\\Users\\Александра\\Documents\\МГТУ\\5 семестр\\РИС\\Python\\outdoor_advertising\\outdoor_advertising\\basket'), 'sql'))
# _sql = []


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def select_dict(dbconfig: dict, _sql:str):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(_sql)
        result = []
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row))) #функция zip из двух списков формирует словарь.
                                                    # Из 1го берет ключ, из 2-го значение.
    return result


#вызов процедуры
def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')

        param_list = []
        for arg in args:            # тут создается цикл, в котором формируется список
            param_list.append(arg)
        print(param_list)
        res = cursor.callproc(proc_name, param_list)
    return res
# метод требует, чтобы был передан список
# плохо обращается с выходными параметрами -> ДОБАВИТЬ ПРОВЕРКУ, СУЩЕСТВУЕТ ЛИ ТАКОЙ ОТЧЕТ


def save_order_with_list(dbconfig: dict, user_id: int, current_basket, provider):
    with DBConnection(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Cursor not created')
        print("created")
        print(user_id)
        summ = session.get('sum')
        _sql1 = provider.get('insert_order.sql', user_id=user_id, tot_cost=summ)
        result1 = cursor.execute(_sql1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print('order_id= ', order_id)
            if order_id:
                for key in current_basket:
                    print(current_basket[key])
                    month_beg = int(current_basket[key]['month_order'])
                    print('month beg type:', type(month_beg))
                    year_beg = int(current_basket[key]['year_order'])
                    duration = int(current_basket[key]['duration'])
                    print('duration type:', type(duration))
                    cost = current_basket[key]['cost']
                    month_end = month_beg + duration
                    year_end = year_beg
                    if int(month_end) > 12:
                        year_end = year_beg + int(month_end / 12)
                        month_end = int(month_end) % 12
                        print('month end type:', type(month_end))
                    _sql3 = provider.get('insert_order_list.sql', id_ordering=order_id, id_billboard=key,
                                         month_beg=month_beg, year_beg=year_beg, duration=duration,
                                         month_end=month_end, year_end=year_end, cost=cost)
                    print(_sql3)
                    print('basket:', current_basket)
                    cursor.execute(_sql3)
                return order_id
