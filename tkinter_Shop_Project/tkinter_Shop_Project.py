import sqlite3
import tkinter

try:
    cnt=sqlite3.connect('shop.db')
    # print("opened database successfully")
except:
    print("an error occurred in db connection")

#---------------create users table---------------
    
# query='''CREATE TABLE users
#     (ID INTEGER PRIMARY KEY,
#     user CHAR(25) NOT NULL,
#     pass CHAR(25) NOT NULL,
#     addr CHAR(50) NOT NULL,
#     comment CHAR(50)
#     )'''
# cnt.execute(query)
# print("Table created successfully")
# cnt.close()

#----------------insert initial record in users table-------------------

# query='''INSERT INTO users (user,pass,addr)
# VALUES("admin","123456789","rasht")'''
# print("data inserted successfully")
# cnt.execute(query)
# cnt.commit()
# cnt.close()

#-----------------create products table-----------------

# query='''CREATE TABLE products
#       (ID INTEGER PRIMARY KEY,
#       pname CHAR(25) NOT NULL,
#       price int NOT NULL,
#       qnt int NOT NULL
#       )'''
# cnt.execute(query)
# print("Table created successfully")
# cnt.close()

#----------------insert initial record in products table-------------------

# query='''INSERT INTO products (pname,price,qnt)
# VALUES("nokia n95",100,10)'''
# print("data inserted successfully")
# cnt.execute(query)
# cnt.commit()
# cnt.close()

#-------------------create finalShop table----------------------------------

# query='''CREATE TABLE finalShop
#     (ID INTEGER PRIMARY KEY,
#     uid int NOT NULL,
#     pid int NOT NULL,
#     qnt int NOT NULL
#     )'''
# cnt.execute(query)
# print("Table created successfully")
# cnt.close()

#----------------functions-------------------

def login():
    global userID
    user=user_txt.get()
    pas=pass_txt.get()
    query='''SELECT id FROM users WHERE user=? AND pass=?'''
    result=cnt.execute(query,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        msg_lbl.configure(text="Wrong Username or Password", fg="red")
        return
    
    userID=rows[0][0]
    
    msg_lbl.configure(text="welcome to your account", fg="green")
    btn_login.configure(state="disabled")
    btn_logout.configure(state="active")
    btn_shop.configure(state="active")
    my_shop_btn.configure(state="active")
    if user=="admin":
        admin_btn.configure(state="active")
    
    user_txt.delete(0,"end")
    pass_txt.delete(0,"end")
    
    user_txt.configure(state="disabled")
    pass_txt.configure(state="disabled")
    
def logout():
    msg_lbl.configure(text="you are logged out now", fg="green")
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    btn_shop.configure(state="disabled")
    user_txt.configure(state="normal")
    pass_txt.configure(state="normal")

def validation(user, pas, cpas, addr):
    if user=="" or pas=="" or cpas=="" or addr=="":
        lbl_msg2.configure(text="Please Fill All the Blanks",fg="red")
        return False
    if len(pas)<8:
        lbl_msg2.configure(text="Password Must Be At least 8 Characters",fg="red")
        return False
    if pas!=cpas:
        lbl_msg2.configure(text="Password and Confirmation Mismatch",fg="red")
        return False
    query=''' SELECT * FROM users WHERE user=?'''
    result=cnt.execute(query,(user,))
    rows=result.fetchall()
    if len(rows)!=0:
        lbl_msg2.configure(text="Username Already Exist!",fg = "red")
        return False
    return True

def final_submit():
    user=txt_user2.get()
    pas=txt_pass2.get()
    cpas=txt_cpas.get()
    addr=txt_addr.get()
    result=validation(user,pas,cpas,addr)
    if not result:
        return
    query ='''INSERT INTO users (user,pass,addr) VALUES (?,?,?)'''
    cnt.execute(query,(user,pas,addr))
    cnt.commit()
    lbl_msg2.configure(text="Submit Done!",fg="green")
    txt_user2.delete(0,"end")
    txt_pass2.delete(0,"end")
    txt_cpas.delete(0,"end")
    txt_addr.delete(0,"end")    
    
def submit():
    global txt_user2,txt_pass2,txt_cpas,txt_addr,lbl_msg2
    win_submit=tkinter.Toplevel(win)
    win_submit.title("Submit Panel")
    win_submit.geometry("350x300")
    
    #-------------------widgets--------------------
    
    lbl_user2=tkinter.Label(win_submit,text="Username: ")
    lbl_user2.pack()
    txt_user2=tkinter.Entry(win_submit,width=20)
    txt_user2.pack()
    
    lbl_pass2=tkinter.Label(win_submit,text="Password: ")
    lbl_pass2.pack()
    txt_pass2=tkinter.Entry(win_submit,width=20)
    txt_pass2.pack()

    lbl_cpas=tkinter.Label(win_submit,text="Password Confirmation: ")
    lbl_cpas.pack()
    txt_cpas=tkinter.Entry(win_submit,width=20)
    txt_cpas.pack()

    lbl_addr=tkinter.Label(win_submit,text="Address: ")
    lbl_addr.pack()
    txt_addr=tkinter.Entry(win_submit,width=40)
    txt_addr.pack()
    
    lbl_msg2=tkinter.Label(win_submit,text="")
    lbl_msg2.pack(pady=10)
    
    btn_submit2=tkinter.Button(win_submit,text="Submit Now",command=final_submit)
    btn_submit2.pack()

    win_submit.mainloop()
    
def update_list():
    query=''' SELECT * FROM products'''
    result=cnt.execute(query)
    rows=result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
        # msg=str(item[0])+"----"+item[1]+"----"+"Price:"+str(item[2])+"----"+"Qnt:"+str(item[3])
        msg=f"{item[0]}----{item[1]}----Price:{item[2]}----QNT:{item[3]}"
        lstbox.insert("end",msg) 
    
def shop_win():
    global txt_id, txt_qnt, lbl_msg2, lstbox
    sh_win=tkinter.Toplevel(win)
    sh_win.geometry("500x500")
    sh_win.title("shopping panel")
    sh_win.resizable(False,False)
    
    #--------------------fetch all products-----------------
    query='''SELECT * FROM products'''
    result=cnt.execute(query)
    result.fetchall()
    
    #-------------------------Listbox-----------------------
    lstbox=tkinter.Listbox(sh_win,width=350)
    lstbox.pack(pady=10)
    
    #--------------------shop widgets---------------------
    lbl_id=tkinter.Label(sh_win,text="Product ID:")
    lbl_id.pack()
    txt_id=tkinter.Entry(sh_win,width=20)
    txt_id.pack()
    
    lbl_qnt=tkinter.Label(sh_win,text="Product QNT:")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(sh_win,width=20)
    txt_qnt.pack()
    
    lbl_msg2=tkinter.Label(sh_win,text="")
    lbl_msg2.pack()
    btn_final_shop=tkinter.Button(sh_win,text="SHOP NOW!", command=final_shop)
    btn_final_shop.pack(pady=5)
    
    #-----------------fetch and insert data into listbox-------------------
    update_list()

    sh_win.mainloop()
    
def final_shop():
    pid=txt_id.get()
    pqnt=txt_qnt.get()
    if (pid=="" or pqnt==""):
        lbl_msg2.configure(text="Please Fill All The Blanks", fg="red")
        return
    query='''SELECT * FROM products WHERE id=?'''
    result=cnt.execute(query,(pid,))
    rows=result.fetchall()
    if len(rows)==0:
        lbl_msg2.configure(text="Error:Wrong Product ID!", fg="red")
        return
    
    real_pqnt=rows[0][3]
    if int(pqnt)>real_pqnt:
        lbl_msg2.configure(text="Error:Not Enough Product Quantity!", fg="red")
        return
    #------------------insert into finalShop table----------------------
    query='''INSERT INTO finalShop (uid,pid,qnt)
            VALUES(?,?,?)'''
    print("data inserted successfully")
    cnt.execute(query, (userID,pid,pqnt))
    cnt.commit()

    #------------------update products table---------------------------
    new_qnt=real_pqnt-int(pqnt)
    query='''UPDATE products SET qnt=? WHERE id=?'''
    cnt.execute(query,(new_qnt,pid))
    cnt.commit()
    lbl_msg2.configure(text="Successfully added to cart", fg="green")
    txt_id.delete(0,"end")
    txt_qnt.delete(0,"end")
    
    #----------------------update listbox------------------------------
    
    update_list()
    
def my_shop():
    win_my_shop=tkinter.Toplevel(win)
    win_my_shop.title("my shopping panel")
    win_my_shop.geometry("400x300")
    win_my_shop.resizable(False,False)
     
    lstbox2=tkinter.Listbox(win_my_shop,width=50)
    lstbox2.pack(pady=10)
     
    
    win_my_shop.mainloop()
    
def insert_product():
    admin_pname=txt_pname.get()
    admin_price=txt_price.get()
    admin_qnt=txt_qnt.get()
    
    if admin_pname=="" or admin_price=="" or admin_qnt=="":
        lbl_msg_admin.configure(text="Please Fill All The Blanks",fg="red")
        return
    
    if (admin_price)<0 or (admin_qnt)<0:
        lbl_msg_admin.configure(text="Wrong Numbers",fg="red")
        return
    
    query='''SELECT * FROM products WHERE pname=?'''
    result=cnt.execute(query,(admin_pname,))
    row=result.fetchone()
    if len(row)>=1:
       lbl_msg_admin.configure(text="Product's Name Already Exists!",fg="red")
       return 
   
    query = ''' INSERT INTO products (pname,price,qnt) VALUES (?,?,?) '''
    cnt.execute(query,(admin_pname,admin_price,admin_qnt))
    cnt.commit()
    lbl_msg_admin.configure(text="Product's data saved successfully!",fg="green")
    txt_pname.delete(0,"end")
    txt_qnt.delete(0,"end")
    txt_price.delete(0,"end")
    
def admin_panel():
     global txt_pname,txt_price,lbl_msg_admin,txt_qnt
     win_admin=tkinter.Toplevel(win)
     win_admin.title("admin panel")
     win_admin.geometry("350x350")
     win_admin.resizable(False,False)
     
     lbl_pname=tkinter.Label(win_admin,text="Product Name: ")
     lbl_pname.pack()
     txt_pname=tkinter.Entry(win_admin,width=15)
     txt_pname.pack()
     
     lbl_price=tkinter.Label(win_admin,text="Price: ")
     lbl_price.pack()
     txt_price=tkinter.Entry(win_admin,width=15)
     txt_price.pack()
     
     lbl_qnt=tkinter.Label(win_admin,text="Quantity: ")
     lbl_qnt.pack()
     txt_qnt=tkinter.Entry(win_admin,width=15)
     txt_qnt.pack()
     
     lbl_msg_admin=tkinter.Label(win_admin,text="")
     lbl_msg_admin.pack()
     
     insert_btn=tkinter.Button(win_admin,text="insert product",command=insert_product)
     insert_btn.pack()
     

     win_admin.mainloop()
    
#-----------------main------------------------

win=tkinter.Tk()
win.title('login')
win.geometry('400x350')

user_lbl=tkinter.Label(win, text="username")
user_lbl.pack()

user_txt=tkinter.Entry(win,width=25)
user_txt.pack()

pass_lbl=tkinter.Label(win,text="password:")
pass_lbl.pack()

pass_txt=tkinter.Entry(win,width=25)
pass_txt.pack()

msg_lbl=tkinter.Label(win,text="")
msg_lbl.pack()

btn_login=tkinter.Button(win,text="Login",width=10,command=login)
btn_login.pack(pady="5")

btn_logout=tkinter.Button(win,text="Logout",state="disabled",width=10,command=logout)
btn_logout.pack(pady="5")

btn_submit=tkinter.Button(win,text="Submit",width=10,command=submit)
btn_submit.pack(pady="5")

btn_shop=tkinter.Button(win,text="Shop",state="disabled",width=10,command=shop_win)
btn_shop.pack(pady="5")

my_shop_btn=tkinter.Button(win,text="My shop",state="disabled",width=10,command=my_shop)
my_shop_btn.pack(pady="5")

admin_btn=tkinter.Button(win,text="Admin Panel",state="disabled",width=10,command=admin_panel)
admin_btn.pack(pady="5")

win.mainloop()












