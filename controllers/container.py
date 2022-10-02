import docker
from flask import jsonify, make_response, Blueprint

from services import container

api = Blueprint('containers_controller', 'containers_controller', url_prefix='/api')


@api.route('/containers')
def container_list():
    try:
        return make_response(jsonify(container.retrieve_containers()), 200)
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)


@api.route('/containers', methods=['POST'])
def run_default_container():
    try:
        return make_response(jsonify(container.run_container()), 201)
    except docker.errors.ImageNotFound as e:
        return make_response(jsonify({"error": "Image Not Found", "details": str(e)}), 500)  # Maybe should be 4xx code
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)


@api.route('/containers/<id>/start', methods=['PUT'])
def start_container(id):
    try:
        return make_response(jsonify(container.start_container(id)), 201)
    except docker.errors.ImageNotFound as e:
        return make_response(jsonify({"error": "Image Not Found", "details": str(e)}), 500)  # Maybe should be 4xx code
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)


@api.route('/containers/<id>/stop', methods=['PUT'])
def stop_container(id):
    try:
        return make_response(jsonify(container.stop_container(id)),
                             202)  # Accepted response code, maybe 200 here as well
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)


@api.route('/containers/<id>/remove', methods=['DELETE'])
def remove_container(id):
    try:
        return make_response(jsonify(container.remove_container(id)), 200)
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)
