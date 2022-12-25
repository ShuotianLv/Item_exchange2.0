import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import csv

def center_window(root, width, height):
    '''
    窗体居中
    :param root: 窗体对象
    :param width: 窗体宽度
    :param height: 窗体高度
    '''
    screen_width = root.winfo_screenwidth()
    screen_height  = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)  # 设置窗口居中参数
    root.geometry(size)

def read_account():
    '''
    读取用户账号密码数据
    :return: 字典
    '''
    with open("account.csv", encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        account_dict = {}
        for row in csv_reader:
            account_dict[row[1]] = row[2]

    return account_dict

def read_account_waiting():
    '''
    读取用户账号密码数据
    :return: 字典
    '''
    with open("account_waiting.csv", encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        account_waiting_dict = {}
        for row in csv_reader:
            account_waiting_dict[row[1]] = row[2]

    return account_waiting_dict

def read_last_id(filename):
    '''
    读取csv文件中最后一行的id
    :return:
    '''
    with open(filename, encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        li = []
        for row in csv_reader:
            li.append(row[0])
        if li == ['id']:
            return 0
        else:
            return int(li[-1])

def write_in_csv(filename, account_c, password_c, gender_c, address_c, number_c, email_c):
    with open(filename, "a", encoding='gbk', newline='') as csvfile:
        #csvfile.write('\r\n')
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([read_last_id('account_waiting.csv') + 1, account_c, password_c, gender_c, address_c, number_c, email_c])

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

def read_admin_account():
    with open("admin_account.csv", encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)
        admin_account_dict = {}
        for row in csv_reader:
            if row[1] == "用户名":
                continue
            admin_account_dict[row[1]] = row[2]

    return  admin_account_dict

def register():

    resWindow = tk.Tk()  # 设置登陆注册对象
    resWindow.title('你帮我助注册系统')
    center_window(resWindow, 600, 375)
    tk.Label(resWindow, text="你帮我助账号注册", font=("黑体", 24)).place(x=300, y=50, anchor=tk.CENTER)
    tk.Label(resWindow, text="请输入您的账号：", font=("宋体", 14)).place(x=120, y=80)
    tk.Label(resWindow, text="请输入您的密码：", font=("宋体", 14)).place(x=120, y=110)
    account_entry = tk.Entry(resWindow,width=24) #账号输入框
    account_entry.place(x=270, y=80)
    password_entry = tk.Entry(resWindow,width=24) #密码输入框
    password_entry.place(x=270, y=110)
    tk.Label(resWindow, text="请选择您的性别：", font=("宋体", 14)).place(x=120, y=140)
    genderBox = ttk.Combobox(resWindow, height=3, width=6, state='readonly', font=("宋体", 14), values=['男', '女', '保密'])   #性别选择框
    genderBox.place(x=270, y=140)
    tk.Label(resWindow, text="请输入您的地址：", font=("宋体", 14)).place(x=120, y=170)
    tk.Label(resWindow, text="请输入您的电话：", font=("宋体", 14)).place(x=120, y=200)
    tk.Label(resWindow, text="请输入您的邮箱：", font=("宋体", 14)).place(x=120, y=230)
    address_entry = tk.Entry(resWindow, width=24)  # address输入框
    address_entry.place(x=270, y=170)
    phnumber_entry = tk.Entry(resWindow, width=24)  # 密码输入框
    phnumber_entry.place(x=270, y=200)
    email_entry = tk.Entry(resWindow, width=24)  # 账号输入框
    email_entry.place(x=270, y=230)

    account_dict = read_account()
    account_dict_wait = read_account_waiting()
    def change_state():
        account_cur = account_entry.get()
        password_cur = password_entry.get()
        if account_cur in account_dict.keys():
            tk.messagebox.showerror('账号已被注册', '账号已被注册，请重输您的账号!')
        elif account_cur in account_dict_wait.keys():
            tk.messagebox.showerror('该账号正在审核中', '该账号注册正在审核中，请重新输入您的账号！')
        else:
            if len(password_cur) < 6 or is_chinese(password_cur) or (" " in password_cur):
                tk.messagebox.showerror('密码格式错误', '请使用大于等于6位的英文或数字，且不包含空格的字符串作为密码！')
            else:
                gender_cur = genderBox.get()
                if not gender_cur:
                    tk.messagebox.showerror('选择性别', '请选择您的性别！')
                else:
                    address_cur = address_entry.get()
                    if not address_cur:
                        tk.messagebox.showerror('输入地址', '请输入您的地址！')
                    else:
                        number_cur = phnumber_entry.get()
                        if not number_cur:
                            tk.messagebox.showerror('输入手机', '请输入您的手机号码！')
                        elif not str.isnumeric(number_cur):
                            tk.messagebox.showerror('号码错误', '请输入格式正确的手机号码！')
                        else:
                            email_cur = email_entry.get()
                            if not email_cur:
                                tk.messagebox.showerror('输入邮箱', '请输入您的电子邮箱！')
                            elif '@' not in email_cur:
                                tk.messagebox.showerror('邮箱无效', '请输入有效的邮箱！')
                            else:
                                write_in_csv("account_waiting.csv", account_cur, password_cur, gender_cur, address_cur, number_cur, email_cur)
                                tk.messagebox.showwarning('注册申请成功', '注册申请成功！待管理员审核通过后使用本软件！')
                                resWindow.destroy()


    #return_button = tk.Button(resWindow, text='返回登陆界面')
    #return_button.place(x=10, y=5)

    log_button = tk.Button(resWindow,text='申请注册账号', command=change_state)
    log_button.place(x=250, y=290, anchor=tk.CENTER)
    resWindow.mainloop()

#register()