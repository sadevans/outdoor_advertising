import os.path

from flask import *
from db_work import *
from sql_provider import SQLProvider
from db_context_manager import DBConnection
from access import *


blueprint_insert = Blueprint('bp_insert', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_insert.route('/get_data', methods=['GET', 'POST'])
@group_required
def get_data():
    dbconfig = current_app.config['db_config']
    if request.method == 'GET':
        return render_template('input_data.html')
    else:
        city = request.form.get('input_city')
        direction = request.form.get('input_direction')
        cost = int(request.form.get('input_cost'))
        billb_size = int(request.form.get('input_size'))
        quality_indicator = int(request.form.get('input_quality'))
        id_owner = int(request.form.get('input_owner'))
        address = 'г.' + request.form.get('input_city') + ' ' + request.form.get('input_street')
        print(address)
        installation_date = request.form.get('input_date')
        print('date:', installation_date)
        with DBConnection(dbconfig) as cursor:
            if cursor is None:
                raise ValueError('Cursor not created')
            if city:
                _sql = provider.get('insert_data.sql', cost=cost, billb_size=billb_size, installation_date=installation_date,
                                    city=city, direction=direction, address=address, quality_indicator=quality_indicator,
                                    id_owner=id_owner)
                cursor.execute(_sql)
                print(_sql)
                message = 'Билборд успешно добавлен'
            return render_template('input_data.html', message=message)
