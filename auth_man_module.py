'''
Main module to control the Authentication of user provided by the app.
'''
from user_module import User
from hashing_module import hashing, checking
from auth_db_conn import DBConnectionInsert, DBConnectionSelect
import getpass

class AuthenticationManager():
    '''
    Main class used to control the authentication of a user registered with
    this class. Instantiate the class with an instance of User and 
    call authenticate(), the class will handle the authentication.
    '''
    def __init__(self, user: User):
        self.user = user   

    def login_check(self) -> list:
        #using the auth_db_conn module to retrieve user details
        db_man = DBConnectionSelect()
        user_details = db_man.fetchone(self.user.username)
        del(db_man)
        return user_details

    def create_account(self, user_details: dict) -> None:
        #using the auth_db_conn module to add a user to the users table
        db_man = DBConnectionInsert()
        db_man.account_create(user_details)
        del(db_man)

    def create_account_form(self) -> None:
        #form requesting users submit their logon details
        flag = True

        while flag == True:
            #loops whilst user provided passwords don't match
            password_1 = getpass.getpass("Please create a password: ")
            password_2 = getpass.getpass("Please retype your password: ")
            if password_1 == password_2:
                flag = False
            else:
                print("Sorry your passwords don't match please try that again.")
        
        email_address = input("Email: ")        
        
        #hashing function returns a generated salt and hash of the password provided
        salt, hash = hashing(password_1)
        
        #dict of users submissions created
        user_details: dict = {
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

        print('\n')
        print('For demonstration purposes, these are the users details held in the db:')
        print('\n')
        print(self.user)
        print('\n')

        #requests user password
        password = getpass.getpass('Enter your password: ')

        #checking function will hash the provided password with salt and
        #compaire it to the users stored hash value returning a bool.
        password_status = checking(self.user.salt, self.user.hash, password)

        if password_status:
            #grantted acces to application
            print('\n You have access to the world!!!!! \n')
        else:
            #denied acces to application
            print("\n You've been done by sha256 hashing!!!! Access Denied \n")

    def authenticate(self) -> None:
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
