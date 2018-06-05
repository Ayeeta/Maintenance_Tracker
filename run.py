from src.user import User
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
usr = User()

@app.route('/auth/signup', methods=['POST'])
def signup_usr():
    info = request.get_json()
    usr.signup(info['id_no'], info['firstname'],info['lastname'],info['department'], info['office'],info['upassword'],info['confirm_password'])
    return jsonify({"Message":"saved successfully"})
    
    




if __name__ == '__main__':
    app.run(debug=True)    
