import docker
from flask import jsonify, make_response, Blueprint, render_template

from services import container

web = Blueprint('containers_web', 'containers_web', url_prefix='/web', template_folder='templates')


@web.route('/containers')
def container_list():
    containers_to_view = container.retrieve_containers()
    return render_template('containers.html', containers=containers_to_view)
