from src.model import User
from flask import Flask, jsonify, request, make_response, Response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'maintenancerepairtracker'
usr = User()

def token_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        token = None
        if 'user-access' in request.headers:
            token = request.headers['user-access']
        if not token:
            return jsonify({'Message':'Token required'}), 401        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = data['id_no']
        except:
            return jsonify({'Message':'Token expired'}), 401
        return func(current_user, *args, **kwargs)
    return decorated_func

@app.route('/api/v2/auth/signup', methods=['POST'])
def signup_usr():
    info = request.get_json()
    if info['id_no'] and info['firstname'] and info['lastname'] and info['upassword'] != "":
        try:
            pwd_encrypt = generate_password_hash(info['upassword'], method='sha256')
            usr.signup(info['id_no'], info['firstname'],info['lastname'],info['department'],
                    info['office'], pwd_encrypt)
        except:
            return jsonify({'Message':'id_no already exists'}), 500
        
        return jsonify({"Message":"saved successfully"}), 200
    return jsonify({'Message':'No content'}), 204

@app.route('/api/v2/auth/login', methods=['POST'])
def login_usr():
    info = request.get_json()
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required"'})
        
    result = usr.login(info['id_no'], info['upassword'])
    if result == None:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required"'})
    else:
        token = jwt.encode({'id_no':info['id_no'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=40)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
    

@app.route('/api/v2/requests/', methods=['GET'])
def get_All():
    return jsonify(usr.get_all())

@app.route('/api/v2/users/requests', methods=['POST'])
@token_required
def create_req(current_user):
    info = request.get_json()
    if info['prob_title'] and info['prob_desc'] and info['req_type'] != "":
        usr.create_request(info['prob_title'], info['prob_desc'],info['req_type'], current_user)
        return jsonify({"Message":"saved successfully"}), 200    
    return jsonify({'Message':'No content'}), 204
    

@app.route('/api/v2/users/requests/<prob_id>',methods=['GET'])
@token_required
def getRequest(current_user, prob_id):
    result = usr.get_request(prob_id)
    if result != None:
        return jsonify(result)    
    return Response("{'Message':'Nothing to show'}", status=404, mimetype='application/json') 
    

@app.route('/api/v2/users/requests',methods=['GET'])
@token_required
def getUReq(current_user):    
    return jsonify(usr.get_userRequest(current_user))

@app.route('/api/v2/users/requests/<prob_id>', methods=['PUT'])
@token_required
def modify_req(current_user, prob_id):
    try:
        info = request.get_json()
        if info['prob_title'] and info['prob_desc'] != "":
            usr.modify_request(prob_id, info['prob_title'], info['prob_desc'])
            return jsonify({"Message":"Edit successful"}),200
        return jsonify({'Message':'No content'}), 204
    except:
        return make_response({'Message':'Bad request'}), 400
    

@app.route('/api/v2/requests/<prob_id>/approve', methods=['PUT'])
def approve_req(prob_id):
    usr.approve_request(prob_id)
    return jsonify({"Message":"Approve successful"}),200
    

@app.route('/api/v2/requests/<prob_id>/disapprove', methods=['PUT'])
def disapprove_request(prob_id):
    usr.disapprove_request(prob_id)
    return jsonify({"Message":"Request Disapproved"}),200

@app.route('/api/v2/requests/<prob_id>/resolve', methods=['PUT'])
def resolve_req(prob_id):
    usr.resolved_request(prob_id)
    return jsonify({"Message":"Request Done.."}),200  

if __name__ == '__main__':
    app.run(debug=True)    
