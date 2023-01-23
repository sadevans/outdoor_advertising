import os.path

from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_schedule = Blueprint('bp_schedule', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_schedule.route('/view_schedule', methods=['GET', 'POST'])
@group_required
def view_schedule():
    columns = ['Месяц начала аренды', 'Год начала аренды', 'Месяц конца аренды', 'Год конца аренды', 'Номер билборда']
    if request.method == 'GET':
        print('я тут нахуй')
        _sql = provider.get('view_schedule.sql')
        product_result, schema = select(current_app.config['db_config'], _sql)
        return render_template('view_schedule.html', schema=columns, result=product_result)