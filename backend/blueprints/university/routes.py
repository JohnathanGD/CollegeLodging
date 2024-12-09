from flask import Blueprint, jsonify
import backend.services.university_service as university_service

university_bp = Blueprint('university', __name__)

@university_bp.route('/search/<string:prefix>')
def search_university(prefix):
    return jsonify(university_service.get_university_data_by_prefix(prefix))

@university_bp.route('/name/<string:name>')
def get_university_by_name(name):
    return jsonify(university_service.get_university_data_by_name(name))

@university_bp.route('/alias/<string:alias>')
def get_university_by_alias(alias):
    return jsonify(university_service.get_university_data_by_alias(alias))

@university_bp.route('/state/<string:state>')
def get_university_by_state(state):
    return jsonify(university_service.get_university_data_by_state(state))

@university_bp.route('/city/<string:city>')
def get_university_by_city(city):
    return jsonify(university_service.get_university_data_by_city(city))

@university_bp.route('/zipcode/<string:zip_code>')
def get_university_by_zipcode(zip_code):
    return jsonify(university_service.get_university_data_by_zipcode(zip_code))

@university_bp.route('/name-or-alias/<string:name>')
def get_university_by_name_or_alias(name):
    return jsonify(university_service.get_university_by_name_or_alias(name))

@university_bp.route('/key/<string:key>/<string:key_type>')
def get_university_by_key(key, key_type):
    return jsonify(university_service.get_university_data_by_key(key, key_type))

@university_bp.route('/all')
def get_all_universities():
    return jsonify(university_service.university_data)