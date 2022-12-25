import tkinter as tk
import tkinter.messagebox
import csv
from user import User, UserStock
from entryWindow import center_window
import tkinter.ttk as ttk

def read_user_w():
    '''
    :return: 列表
    '''
    with open("account_waiting.csv", encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        user_w_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            user_cur = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            user_w_list.append(user_cur)
    return user_w_list

def read_type_c():
    with open('types.csv', encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        type_dict = {}
        for row in csv_reader:
            cha_l = row[1].split(sep=',')
            type_dict[row[0]] = cha_l
    return type_dict

def update_a(t, Users):
    '''
    在t列表里更新最新的stock对象库存情况
    :param t: the treeview
    '''
    for child in t.get_children():
        t.delete(child)
    for item in Users.accounts:
        t.insert('', tk.END, values=(item.id, item.account, item.password, item.gender, item.address, item.phonenumber, item.email))

def update_ty(t, type_dict):
    for child in t.get_children():
        t.delete(child)
    for type in list(type_dict.keys()):
        t.insert('', tk.END, values=(type, type_dict[type]))

def read_last_id(filename):
    '''
    读取csv文件中最后一行的id
    :return:
    '''
    with open(filename, encoding='gbk', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        li = []
        for row in csv_reader:
            li.append(row[0])
        if li == ['id']:
            return 0
        else:
            return int(li[-1])

def write_in_csv(filename, user):
    with open(filename, "a", encoding='gbk', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([read_last_id('account.csv') + 1, user.account, user.password, user.gender, user.address, user.phonenumber, user.email])

def write_in_type(ty_cur, cha_cur):
    with open('types.csv', "a", encoding='gbk', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([ty_cur, cha_cur])

def delete_item_csv(item_index, filename):
    r = csv.reader(open(filename, encoding='gbk', newline=''))
    lines = list(r)
    for line in lines:
        if line[0] == str(item_index):
            lines.remove(line)
            break
    writer = csv.writer(open(filename, 'w', encoding='gbk', newline=''))
    writer.writerows(lines)

def admin():
    adminWindow = tk.Tk()
    adminWindow.title('你帮我助管理员界面')
    center_window(adminWindow, 880, 700)


    tk.Label(adminWindow, text='待审核注册用户', font=("黑体",20)).place(x=430,y=45, anchor=tk.CENTER)
    columns = ['ID', '用户名', '密码', '性别', '地址', '联系电话', '电子邮箱']
    tree = ttk.Treeview(adminWindow, show="headings", height=10, columns=columns)
    tree.column('ID', width=40, anchor=tk.CENTER,stretch=False)
    tree.column('用户名', width=120, anchor=tk.CENTER)
    tree.column('密码', width=120, anchor=tk.CENTER)
    tree.column('性别', width=40, anchor=tk.CENTER)
    tree.column('地址', width=145, anchor=tk.CENTER)
    tree.column('联系电话', width=145, anchor=tk.CENTER)
    tree.column('电子邮箱', width=145, anchor=tk.CENTER)
    tree.heading('ID', text='ID')
    tree.heading('用户名', text='用户名')
    tree.heading('密码', text='密码')
    tree.heading('性别', text='性别')
    tree.heading('地址', text='地址')
    tree.heading('联系电话', text='联系电话')
    tree.heading('电子邮箱', text='电子邮箱')
    tree.place(x=50, y=60)

    UserS = UserStock(read_user_w())
    update_a(tree, UserS)
    def agree_ac():
        res = tk.messagebox.askyesnocancel('提示！', '是否确认该用户注册？')
        if res:
            item_index = tree.item(tree.selection()[0], "values")[0]
            for user_cur in UserS.accounts:
                if user_cur.id == item_index:
                    break
            user_append = user_cur
            UserS.accounts.remove(user_cur)
            update_a(tree, UserS)
            write_in_csv('account.csv', user_append)
            delete_item_csv(item_index, 'account_waiting.csv')

    ag_button = tk.Button(adminWindow, text='通过该用户注册', background='white',command=agree_ac).place(x=50, y=300)

    def refuse_ac():
        res = tk.messagebox.askyesnocancel('提示！', '是否拒绝该用户注册？')
        if res:
            item_index = tree.item(tree.selection()[0], "values")[0]
            for user_cur in UserS.accounts:
                if user_cur.id == item_index:
                    break
            UserS.accounts.remove(user_cur)
            update_a(tree, UserS)
            delete_item_csv(item_index, 'account_waiting.csv')

    refu_button = tk.Button(adminWindow, text='拒绝该用户注册', background='white',command=refuse_ac).place(x=200, y=300)

    tk.Label(adminWindow, text='添加/修改物品类型', font=("黑体", 20)).place(x=430, y=350, anchor=tk.CENTER)

    tk.Label(adminWindow, text="新的类型名称：", font=("宋体", 14)).place(x=50, y=380)
    type_entry = tk.Entry(adminWindow, width=15)
    type_entry.place(x=170, y=380)

    tk.Label(adminWindow, text="新的类型属性：", font=("宋体", 14)).place(x=350, y=380)
    addr = tk.StringVar()
    addr.set("（用中文逗号区分不同属性）")
    cha_entry = tk.Entry(adminWindow, width=27, textvariable=addr)
    cha_entry.place(x=480, y=380)


    tree2 = ttk.Treeview(adminWindow, show="headings", height=8, columns=['物品类型', '物品属性'])
    tree2.column('物品类型', width=170, anchor=tk.CENTER)
    tree2.column('物品属性', width=460, anchor=tk.CENTER)
    tree2.heading('物品类型', text='物品类型')
    tree2.heading('物品属性', text='物品属性')
    tree2.place(x=50, y=420)
    type_dic_s = read_type_c()
    update_ty(tree2, type_dic_s)

    def add_type():
        ty_cur = type_entry.get()
        char_cur = cha_entry.get()
        if not ty_cur:
            tk.messagebox.showerror('未输入类型', '请输入要添加的物品类型！')
        elif ty_cur in list(type_dic_s.keys()):
            tk.messagebox.showerror('类型已存在', '该物品类型已存在！')
        else:
            if char_cur == "（用中文逗号区分不同属性）":
                tk.messagebox.showerror('未输入属性', '请输入该类型的属性！')
            elif '。' in char_cur or ',' in char_cur or '.' in char_cur or '？' in char_cur or '!' in char_cur:
                tk.messagebox.showerror('分隔符错误', '请使用中文逗号作为属性间的分隔符！')
            else:
                type_dic_s[ty_cur] = char_cur.split(sep='，')
                write_in_type(ty_cur, char_cur)
                update_ty(tree2, type_dic_s)

    type_e_button = tk.Button(adminWindow, text='确认添加',command=add_type).place(x=730, y=380)

    def corr_type():
        item_index = tree2.item(tree2.selection()[0], "values")[0]
        newWin =tk.Tk()
        newWin.title('修改 {} 类型'.format(item_index))
        center_window(newWin, 400,200)

        tk.Label(newWin, text="修改后的类型名称：", font=("宋体", 14)).place(x=50, y=40)
        ty_entry = tk.Entry(newWin, width=18)
        ty_entry.place(x=210, y=40)
        tk.Label(newWin, text="修改后的类型属性：", font=("宋体", 14)).place(x=50, y=80)
        c_entry = tk.Entry(newWin, width=18)
        c_entry.place(x=210, y=80)

        def return_ty():
            type_n = ty_entry.get()
            c_n = c_entry.get()
            if not type_n:
                tk.messagebox.showerror('未输入类型', '请输入要修改的物品类型！')
            elif type_n in list(type_dic_s.keys()) and type_n != item_index:
                tk.messagebox.showerror('类型已存在', '该物品类型已存在！')
            else:
                if not c_n:
                    tk.messagebox.showerror('未输入属性', '请输入该类型的属性！')
                elif '。' in c_n or ',' in c_n or '.' in c_n or '？' in c_n or '!' in c_n:
                    tk.messagebox.showerror('分隔符错误', '请使用中文逗号作为属性间的分隔符！')
                else:
                    del type_dic_s[item_index]
                    delete_item_csv(item_index, 'types.csv')
                    type_dic_s[type_n] = c_n.split(sep='，')
                    write_in_type(type_n, c_n)
                    update_ty(tree2, type_dic_s)
                    newWin.destroy()

        check_bu = tk.Button(newWin, text='确认修改',command=return_ty).place(x=200,y=150, anchor=tk.CENTER)

    correct_button = tk.Button(adminWindow, text='修改该类型',command=corr_type).place(x=715, y=430)

    def delete_type():
        item_index = tree2.item(tree2.selection()[0], "values")[0]
        del type_dic_s[item_index]
        delete_item_csv(item_index, 'types.csv')
        update_ty(tree2, type_dic_s)

    delete_button = tk.Button(adminWindow, text='删除该类型',command=delete_type).place(x=715, y=480)


    def exit_window():
        res = tk.messagebox.askyesnocancel('提示', '是否退出软件？')
        if res:
            adminWindow.destroy()

    exit_button = tk.Button(adminWindow, text='退出软件',command=exit_window).place(x=440, y=650, anchor=tk.CENTER)
    adminWindow.mainloop()



