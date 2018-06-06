from src.user import User
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
usr = User()

@app.route('/auth/signup', methods=['POST'])
def signup_usr():
    info = request.get_json()
    usr.signup(info['id_no'], info['firstname'],info['lastname'],info['department'], info['office'],info['upassword'],info['confirm_password'])
    return jsonify({"Message":"saved successfully"}), 200

@app.route('/auth/login', methods=['POST'])
def login_usr():
    info = request.get_json()
    result = usr.login(info['id_no'], info['upassword'])
    if result == []:
        return jsonify({"Message":"Unauthorised"}), 401
    else:
        return jsonify({"Message":"You are logged in"}), 200

@app.route('/requests/', methods=['GET'])
def get_All():
    return jsonify(usr.get_all())

@app.route('/users/requests/', methods=['POST'])
def create_req():
    info = request.get_json()
    usr.create_request(info['prob_title'], info['prob_desc'],info['req_type'],info['id_no'])
    return jsonify({"Message":"saved successfully"}), 200

@app.route('/users/requests/<prob_id>',methods=['GET'])
def getRequest(prob_id):
    return jsonify(usr.get_request(prob_id))

@app.route('/users/<id_no>/requests',methods=['GET'])
def getUReq(id_no):
    return jsonify(usr.get_userRequest(id_no))

@app.route('/users/requests/<prob_id>', methods=['PUT'])
def modify_req(prob_id):
    info = request.get_json()
    usr.modify_request(prob_id, info['prob_title'], info['prob_desc'])
    return jsonify({"Message":"Edit successful"}),200

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
