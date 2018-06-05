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
        #self.cur.execute()
        pass

    def create_request(self, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        pass

    def modify_request(self, prob_id, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        pass
    
    def delete_request(self, prob_id, prob_title, prob_desc, req_type, id_no):
        #fail if id_no doesn't exist
        pass

    def get_All(self):
        pass
    
    def get_request(self, prob_id):
        pass