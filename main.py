from mainWindow import mainWindow
from entryWindow import enter
from user import User, UserStock
from admin_enter import admin
import csv

def read_user_w():
    '''
    :return: 列表
    '''
    with open("account.csv", encoding='gbk', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        user_w_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            user_cur = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            user_w_list.append(user_cur)
    return user_w_list


if __name__ == '__main__':
    UserS = UserStock(read_user_w())
    s, account = enter()

    for users in UserS.accounts:
        if users.account == account:
            break

    if s == 1:
        mainWindow(users)
    elif s == 0:
        admin()

