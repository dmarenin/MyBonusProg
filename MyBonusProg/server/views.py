from flask import render_template, request, jsonify
import server.api_func as api_func
from server.conf import *
from server import app
import logging
import json


FORMAT = '%(asctime)s - %(levelname)s - %(message)s \n\r'

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG, format=FORMAT)

HEADERS = {"Content-type": "application/json",
           "Access-Control-Allow-Origin": "*", 
           "Access-Control-Expose-Headers": "Access-Control-Allow-Origin",
           "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"}

@app.route('/')
@app.route('/index')
def index():
    return 'it`s works', 200, HEADERS

@app.errorhandler(KeyError)
def handle_invalid_usage(error):
    str_error = "KeyError: %s" % error
        
    func_log = logging.error

    func_log(str_error)

    response = jsonify(str_error)
    response.status_code = 500
    response.content_type = 'text/plain; charset=utf-8'
    
    return response

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    str_error = "Exception: %s" % error

    func_log = logging.error

    func_log(str_error)

    response = jsonify(str_error)
    response.status_code = 500
    response.content_type = 'text/plain; charset=utf-8'
    
    return response
   
@app.route('/info', methods=['GET'])
def info():
    args = request.args.to_dict()
    
    res = api_func.info(args)

    return result(res, args)

@app.route('/purchase', methods=['GET'])
def purchase():
    args = request.args.to_dict()
    
    res = api_func.purchase(args)

    return result(res, args)

@app.route('/revert', methods=['GET'])
def revert():
    args = request.args.to_dict()
    
    res = api_func.revert(args)

    return result(res, args)

@app.route('/accrue_bonuses', methods=['GET'])
def accrue_bonuses():
    args = request.args.to_dict()
    
    res = api_func.accrue_bonuses(args)

    return result(res, args)

@app.route('/delete_card', methods=['GET'])
def delete_card():
    args = request.args.to_dict()
    
    res = api_func.delete_card(args)

    return result(res, args)

def result(res, args):
    res = json.dumps(res, default=json_serial)
    
    func_log = logging.info

    func_log(res)

    return res, 200, HEADERS

def json_serial(obj):
    from datetime import datetime, date
    import decimal
    if isinstance(obj, (datetime, date)):
       return obj.isoformat()

    if isinstance(obj, decimal.Decimal):
       return float(obj)
    pass

