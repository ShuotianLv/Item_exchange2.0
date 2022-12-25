class User:
    def __init__(self, id, account, password, gender, address, phonenumber, email):
        self.id = id
        self.account = account
        self.password = password
        self.gender = gender
        self.address = address
        self.phonenumber = phonenumber
        self.email = email
class UserStock:
    def __init__(self, account_list):
        self.accounts = account_list
