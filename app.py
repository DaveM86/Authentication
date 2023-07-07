from user_module import User
from auth_man_module import AuthenticationManager

def logon_form() -> str:
    username = input("Username: ")
    return username

def main():
    username = logon_form()
    user = User(username)
    auth_man = AuthenticationManager(user)
    auth_man.authenticate()

if __name__=='__main__':
    main()