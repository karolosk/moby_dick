from flask import jsonify, make_response, Blueprint, render_template

from services import container

web = Blueprint('index', 'index', url_prefix='/web', template_folder='templates')


@web.route('/')
def container_list():
    return render_template('index.html')
