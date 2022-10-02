import docker
from services import image
from flask import Flask, render_template, jsonify, make_response, request, Blueprint

api = Blueprint('image_controller', 'image_controller', url_prefix='/api')


@api.route('/images')
def image_list():
    try:
        return make_response(jsonify(image.retrieve_images()), 200)
    except (docker.errors.APIError) as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)


@api.route('/images/build', methods=['POST'])
def build_image():
    try:
        new_image = image.create_image(request.args)
        status_code = image.identify_status_code(new_image)
        return make_response(jsonify(new_image), status_code)
    except (docker.errors.APIError, docker.errors.BuildError) as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)
    except Exception as e:
        return make_response(jsonify({"error": "Application error", "details": str(e)}), 400)


@api.route('/images/delete', methods=['DELETE'])
def delete_image():
    try:
        return make_response(jsonify(image.delete_image(request.args['tags'])), 202)
    except docker.errors.APIError as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)