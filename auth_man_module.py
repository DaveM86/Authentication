'''
We need a rake of detail here!!!!!!!!
'''

from user_module import User
from hashing_module import hashing, checking
import sqlite3


class AuthenticationManager():
    def __init__(self, user: User):
        self.user = user
        
    def set_connection(self):
        return sqlite3.connect('users.db')
    
    def login_check(self) -> list:
        #setup connection to db
        conn = self.set_connection()
        cur = conn.cursor()
        #get user details from user table
        cur.execute("SELECT * FROM users WHERE username = ?;",(self.user.username,))
        user_details = cur.fetchone()
        conn.commit()
        conn.close()
        return (user_details)

    def create_account(self, user_details: dict) -> None:
        conn = self.set_connection()
        cur = conn.cursor()
        cur.execute("""INSERT into users
                    (username, email_address, salt, hash) 
                    values(?, ?, ?, ?);""", 
                    (
                        user_details['username'], 
                        user_details['email_address'], 
                        user_details['salt'], 
                        user_details['hash'],
                    )
                    )
        print('Account Created')
        conn.commit()
        conn.close()

    def create_account_form(self) -> None:
        #form requesting users submit their logon details
        flag = True
   
        while flag == True:
            password_1 = input("Please create a password: ")
            password_2 = input("Please retype your password: ")
            if password_1 == password_2:
                flag = False
            else:
                print("Sorry your passwords don't match please try that again.")
        
        email_address = input("Email: ")
        
        
        salt, hash = hashing(password_1)
        
        #dict of users submissions created
        user_details = {
                        'username':self.user.username,
                        'email_address':email_address,
                        'salt':salt,
                        'hash':hash,
                        }
        
        #details passed for account creation
        self.create_account(user_details)

        del(password_1)
        del(password_2)


    def password_form(self) -> None:
        user_details = self.login_check()
        self.user.salt = user_details[2]
        self.user.hash = user_details[3]
        self.user.email_address = user_details[1]

        password = input('Enter your password: ')
        password_status = checking(self.user.salt, self.user.hash, password)
        if password_status:

            print('\n You have access to the world!!!!! \n')
        else:
            print("\n You've been done by sha256 hashing!!!! Access Denied \n")
        print(self.user.__dict__)

    def authenticate(self):
        logged_in = False
        while not logged_in:
            user_details = self.login_check()
            if user_details:
                self.password_form()
                logged_in = True
            else:
                print ("It looks like you don't have an account, let's create one")
                self.create_account_form()
