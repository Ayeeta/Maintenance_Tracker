from src.user import User
from flask import Flask, jsonify, request, make_response
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

@app.route('/auth/signup', methods=['POST'])
def signup_usr():
    info = request.get_json()
    pwd_encrypt = generate_password_hash(info['upassword'], method='sha256')
    usr.signup(info['id_no'], info['firstname'],info['lastname'],info['department'], info['office'], pwd_encrypt)
    return jsonify({"Message":"saved successfully"}), 200

@app.route('/auth/login', methods=['POST'])
def login_usr():
    info = request.get_json()
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required"'})
        
    result = usr.login(info['id_no'], info['upassword'])
    if result == []:
        return make_response('Unauthorized',401,{'WWW-Authenticate':'Basic realm="Login required"'})
    else:
        token = jwt.encode({'id_no':info['id_no'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=40)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')}),200
    

@app.route('/requests/', methods=['GET'])
def get_All():
    return jsonify(usr.get_all())

@app.route('/users/requests', methods=['POST'])
@token_required
def create_req(current_user):
    info = request.get_json()
    usr.create_request(info['prob_title'], info['prob_desc'],info['req_type'],info['id_no'])
    return jsonify({"Message":"saved successfully"}), 200
    

@app.route('/users/requests/<prob_id>',methods=['GET'])
@token_required
def getRequest(current_user, prob_id):
    return jsonify(usr.get_request(prob_id))

@app.route('/users/requests',methods=['GET'])
@token_required
def getUReq(current_user):    
    return jsonify(usr.get_userRequest(current_user))

@app.route('/users/requests/<prob_id>', methods=['PUT'])
@token_required
def modify_req(current_user, prob_id):
    try:
        info = request.get_json()
        usr.modify_request(prob_id, info['prob_title'], info['prob_desc'])
        return jsonify({"Message":"Edit successful"}),200
    except:
        return jsonify({"Message":"Not modified"}), 304

@app.route('/requests/<prob_id>/approve', methods=['PUT'])
def approve_req(prob_id):
    
    usr.approve_request(prob_id)
    return jsonify({"Message":"Approve successful"}),200

@app.route('/requests/<prob_id>/disapprove', methods=['PUT'])
def disapprove_request(prob_id):
    usr.disapprove_request(prob_id)
    return jsonify({"Message":"Request Disapproved"}),200

@app.route('/requests/<prob_id>/resolve', methods=['PUT'])
def resolve_req(prob_id):
    usr.resolved_request(prob_id)
    return jsonify({"Message":"Request Done.."}),200 
    

if __name__ == '__main__':
    app.run(debug=True)    
