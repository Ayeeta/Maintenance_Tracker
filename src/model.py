from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

class User:
    """The User class performs queries for the user to the database
    """

    def __init__(self):
        self.conn = psycopg2.connect("dbname=Maintenance_TrackerDB user=postgres password=sap")
        self.cur = self.conn.cursor()       
        
    
    def signup(self, ID_No, fname, lname, department, office, upassword):
        
        self.cur.execute("Insert into users values(%s,%s,%s,%s,%s,%s)",
                          (ID_No, fname, lname, department, office, upassword))
        self.conn.commit()

    def find(self, Id_no):
        self.cur.execute("Select * from urequests where id_no ='{}'".format(Id_no))

    def login(self,Id_no,usrpwd):
        self.cur.execute("select id_no, upassword from users where id_no='{}'".format(Id_no))
        results =  self.cur.fetchall()
        pwd_harsh = ""
        for result in results:
            pwd_harsh = result[1]        
        if check_password_hash(pwd_harsh, usrpwd) == True:
            return results       

    def create_request(self, prob_title, prob_desc, req_type, id_no):
        r_status = 'unapproved'
        self.cur.execute("Insert into urequests(prob_title, prob_desc, req_type, id_no, req_status) values(%s,%s,%s,%s,%s)",
         (prob_title, prob_desc, req_type, id_no, r_status))
        self.conn.commit()

    def modify_request(self, prob_id, prob_title, prob_desc):
        prob_id = int(prob_id)
        r_status = 'unapproved'
        result = self.cur.execute("Update urequests set prob_title = '{}', \
            prob_desc = '{}' where prob_id = '{}' and req_status = '{}'".format(prob_title, prob_desc, prob_id,r_status ))
        self.conn.commit()
        return result
    
    def delete_request(self, prob_id, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        pass
    
    def check_probid(self, prob_id):
        self.cur.execute("select * from urequests where prob_id='{}'".format(prob_id))
        results =  self.cur.fetchall()
        if results == []:
            return False
        return True  
    
    def check_status(self, prob_id):
        r_status = 'Approved'
        self.cur.execute("Select * from urequests where prob_id='{}' and req_status='{}'".format(prob_id, r_status))
        results = self.cur.fetchall()
        if results != []:
            return True
        return False

    def approve_request(self, prob_id):
        status = "Approved"
        self.cur.execute("Update urequests set req_status = '{}'\
                          where prob_id = '{}'".format(status, prob_id))
        self.conn.commit()

    def disapprove_request(self, prob_id):
        status = "Disapproved"
        self.cur.execute("Update urequests set req_status = '{}'\
                          where prob_id = '{}'".format(status, prob_id))
        self.conn.commit()

    def resolved_request(self, prob_id):
        status = "Resolved"
        self.cur.execute("Update urequests set req_status = '{}' \
                          where prob_id = '{}'".format(status, prob_id))
        self.conn.commit()

    def get_all(self):
        self.cur.execute("Select prob_id, prob_title, prob_desc, \
                          req_type, post_date, id_no, req_status from urequests")
        results = self.cur.fetchall()
        result_dict = {}
        result_list = []
        for result in results:
            result_dict['prob_id'] = result[0]
            result_dict['prob_title'] = result[1]
            result_dict['prob_desc'] = result[2]
            result_dict['req_type'] = result[3]
            result_dict['post_date'] = result[4]
            result_dict['id_no'] = result[5]
            result_dict['req_status'] = result[6]
            result_list.append(result_dict)
            result_dict = {}        
        return result_list

    def get_userRequest(self, ID_No):
        self.cur.execute("Select  * from urequests where id_no = '{}'".format(ID_No))
        results = self.cur.fetchall()
        result_dict = {}
        result_list = []
        for result in results:
            result_dict['prob_id'] = result[0]
            result_dict['prob_title'] = result[1]
            result_dict['prob_desc'] = result[2]
            result_dict['req_type'] = result[3]
            result_dict['post_date'] = result[4]
            result_dict['id_no'] = result[5]
            result_dict['req_status'] = result[6]
            result_list.append(result_dict)
            result_dict = {}        
        return result_list
    
    def get_request(self, prob_id):
        self.cur.execute("Select prob_id, prob_title, prob_desc, req_type,"+ 
        "post_date, id_no, req_status from urequests where prob_id = '{}'".format(prob_id))
        results = self.cur.fetchall()
        result_dict = {}
        result_list = []
        for result in results:
            result_dict['prob_id'] = result[0]
            result_dict['prob_title'] = result[1]
            result_dict['prob_desc'] = result[2]
            result_dict['req_type'] = result[3]
            result_dict['post_date'] = result[4]
            result_dict['id_no'] = result[5]
            result_dict['req_status'] = result[6]
            result_list.append(result_dict)
            result_dict = {}        
        return result_list
