import psycopg2

class User:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=Maintenance_TrackerDB user=postgres password=sap")
        self.cur = self.conn.cursor()       
        
    
    def signup(self, ID_No, fname, lname, department, office, upassword, confirm_password):
        self.cur.execute("Insert into users values(%s,%s,%s,%s,%s,%s,%s)",
        (ID_No, fname, lname, department, office, upassword, confirm_password))
        self.conn.commit()
        

    def login(self, ID_No, usrpwd):
        self.cur.execute("Select id_no, upassword from users where id_no=%s AND upassword=%s",(ID_No, usrpwd))
        return self.cur.fetchall()      
        

    def create_request(self, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        self.cur.execute("Insert into urequests(prob_title, prob_desc, req_type, id_no) values(%s,%s,%s,%s)",
         (prob_title, prob_desc, req_type, id_no))
        self.conn.commit()

    def modify_request(self, prob_id, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        prob_id = int(prob_id)
        self.cur.execute("Insert into urequest(prob_title, prob_desc, req_type) values(%s,%s, %s) where prob_id=%s",
         (prob_title, prob_desc, req_type), prob_id)
    
    def delete_request(self, prob_id, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        pass

    def get_all(self):
        self.cur.execute("Select prob_id, prob_title, prob_desc, req_type, post_date, id_no, req_status from urequests")
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
        pass