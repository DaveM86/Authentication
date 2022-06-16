'''
Main module to control the Authentication of user provided by the app.
'''
from user_module import User
from hashing_module import hashing, checking
import sqlite3


class AuthenticationManager():
    #register the user with the class that requires authentication
    #user is a class it's self, subclass of UserInterface
    def __init__(self, user: User):
        self.user = user
        
    def set_connection(self):
        #set connection to the sqllite database
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
        #setup connection to users db
        conn = self.set_connection()
        cur = conn.cursor()
        #add user to table
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
            #loops whilst user provided passwords don't match
            password_1 = input("Please create a password: ")
            password_2 = input("Please retype your password: ")
            if password_1 == password_2:
                flag = False
            else:
                print("Sorry your passwords don't match please try that again.")
        
        email_address = input("Email: ")        
        
        #hashing function returns a generated salt and hash of the password provided
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
        #clean up stored passwords
        del(password_1)
        del(password_2)


    def password_form(self) -> None:
        #pull user details from user database.
        user_details = self.login_check()
        self.user.salt = user_details[2]
        self.user.hash = user_details[3]
        self.user.email_address = user_details[1]
        #requests user password
        password = input('Enter your password: ')
        #checking function will hash the provided password with salt and
        #compaire it to the users stores hash value returning a bool.
        password_status = checking(self.user.salt, self.user.hash, password)
        if password_status:
            #grantted acces to application
            print('\n You have access to the world!!!!! \n')
        else:
            #denied acces to application
            print("\n You've been done by sha256 hashing!!!! Access Denied \n")
        print(self.user.__dict__)

    def authenticate(self):
        #function called by the app and controls the authentication
        logged_in = False
        while not logged_in:
            user_details = self.login_check()
            #check to see if the user exists in the db
            if user_details:
                #proceed to password
                self.password_form()
                logged_in = True
            else:
                #create an account
                print ("It looks like you don't have an account, let's create one")
                self.create_account_form()
