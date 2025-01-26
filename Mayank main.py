import os       # Import os module for operating system-related functionality.
import subprocess       # Import subprocess module for installing the required packages.
import sys      # Import sys module for system-related functionality.

try:subprocess.check_call(["pip", "--version"])
except subprocess.CalledProcessError:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    batch_dir = current_directory.replace('Code', '') + 'run_me_script.bat'
    subprocess.call(batch_dir, shell=True)

packages=["pmw", "pillow", "opencv-python-headless", "customtkinter", "requests"]
for package in packages:
    try:subprocess.check_call([sys.executable, "-m", "pip", "show", package])
    except subprocess.CalledProcessError:subprocess.run(["pip", "install", package], check=True)

import customtkinter as CTk         # Import customtkinter as CTk for custom tkinter widgets and functionality.
import tkinter as tk        # Import tkinter for creating the graphical user interface.
from tkinter import *       # Import necessary components from tkinter for GUI development.
from tkinter import ttk         # Import ttk module for themed widgets in tkinter.
import mysql.connector as mc        # Import mysql.connector to connect to a MySQL database.
import datetime         # Import datetime module to work with dates and times.
from datetime import date       # Import the date class from datetime for date-related operations.
import time         # Import time module for time-related functionality.
import re       # Import the re module for regular expressions.
from PIL import Image, ImageTk          # Import Image and ImageTk from the PIL (Pillow) library for image  handling.
import cv2          # Import cv2 library for video  handling.
import Pmw          # Import Pmw (Python Mega Widgets) for additional and enhanced tkinter widgets.
import requests     #Import requests module to fetch the credentials for connection of database over the internet.

CTk.set_appearance_mode('dark')

class Dateerror(Exception):pass             #Exception raised for errors related to date inputs.
class IncompleteDataerror(Exception):pass       #Exception raised for incomplete data during a booking.
class RoomBookederror(Exception):pass       #Exception raised for errors related to room booking.
class IDException(Exception):pass               #Exception raised for errors related to room booking.

#This function switches the application between offline and online modes    
def switch():
    global n,ask_window

    if n==1:
        ask_window.destroy()
        offline()
    else:
        tk.messagebox.showinfo("Connection switched","You have switched to online mode and are currently connected to our remote server")
        ask_window.destroy()
        online()
#Retrieve and return the rental information for a room specified by the key           
def rent_func(x):
    global rooms_dict
    return rooms_dict.get(x)
#This function attempts to destroy various global window instances
def back():
    global sign_window,log_window,del_window,off_win

    try:off_win.destroy()
    except:pass
    try:sign_window.destroy()
    except:pass
    try:log_window.destroy()
    except:pass
    try:del_window.destroy()
    except:pass
    
    ask()
#This function displays an exit confirmation message    
def ask_exit():
    global ask_window

    exit_confirmation=tk.messagebox.askyesno("Exit Confirmation","Do you wish to exit?")
    if exit_confirmation==True:
        tk.messagebox.showinfo("Exit message","You have exited the program, and the connection is now closed.")
        con.close()
        ask_window.destroy()
#Create and place buttons in the main application window for various actions.
def ask_buttons():
    global ask_window

    ask_window.btn1=CTk.CTkButton(ask_window,text='Log-in', command=loginwindow,width=100, height=55, font=(('arial',20,'bold'))).place(x=105,y=250)
    ask_window.btn2=CTk.CTkButton(ask_window,text='Sign-in', command=signinwindow,width=100, height=55, font=(('arial', 20,'bold'))).place(x=105,y=325)
    ask_window.btn3=CTk.CTkButton(ask_window,text='Delete', command=deletewindow,width=100, height=55, font=(('arial',20,'bold'))).place(x=105,y=400)
    ask_window.btn4=CTk.CTkButton(ask_window,text='Exit', command=ask_exit,width=100, height=55, font=(('arial', 20,'bold'))).place(x=105,y=475)
#Create and display the main application window for the Hotel Management System.
def ask():
    global ask_window,n,image,photo,intro_window

    try:intro_window.destroy()
    except:pass
    
    ask_window=CTk.CTk();ask_window.geometry('300x700+525+0');ask_window.title("Hotel Management System");ask_window.resizable(0,0)
    
    current_directory=os.path.dirname(os.path.abspath(__file__))
    image_dir=current_directory.replace('Code','')+'Media\\Images\\Logo.png'
    image=Image.open(image_dir)

    image=image.resize((150,100),Image.LANCZOS)
    photo=ImageTk.PhotoImage(image)
    
    lb=Label(ask_window,image=photo,borderwidth=0)
    lb.place(x=75,y=20)
        
    label=Label(ask_window,font=('arial',24,'bold'),text="Hotel Manager",padx=2,bg="#282424",fg="white")
    label.place(x=35,y=130)

    ask_buttons()

    if n==1:connection_status=Label(ask_window,font=('arial',6,'bold'),text="@You are connected to a remote server.",padx=2,bg="#282424",fg="white")
    else:connection_status=Label(ask_window,font=('arial',6,'bold'),text="@You are connected to a localhost.",padx=2,bg="#282424",fg="white")
    connection_status.place(x=0,y=668)
    
    ask_window.btn5=CTk.CTkButton(ask_window,text='switch',command=switch,width=50, height=25, font=(('arial', 10,'bold'))).place(x=160,y=665)
    ask_window.mainloop()
# Create and display the main application window for the Hotel Management System.  
def intro():
    global intro_window,image_dir,image,photo
#This function updates the text of a label in a gradual manner to create a fade-in effect.
    def fade_in_label(label,x):
        def update_text(i):
            global intro_window

            if i<= len(x):
                label.config(text=x[:i])
                i+=1
                intro_window.after(100,update_text, i)
        update_text(0)
#This function creates a label with the specified text, font, and position on the introductory window.
    def xyz(x,y,z,font):
        txt=x
        label2=Label(intro_window,text=txt,font=font,fg='white',bg='#282424',borderwidth=0)
        label2.place(x=z,y=y)
        fade_in_label(label2,txt)
#This function gradually increases the alpha value of the image to achieve a fade-in effect.
    def fade_in_effect(label, image, alpha):
        if alpha < 255:
            alpha += 5 
            if alpha > 255:
                alpha = 255
            new_image = Image.new("RGBA", image.size)
            new_image.paste(image, (0, 0))
            new_image.putalpha(alpha)
            label.img = ImageTk.PhotoImage(new_image)
            label.config(image=label.img)
            label.after(50, fade_in_effect, label, image, alpha)

    intro_window=CTk.CTk();intro_window.geometry('600x500+350+100');intro_window.title("Hotel Management System");intro_window.resizable(0,0)
    
    try:
        current_directory=os.path.dirname(os.path.abspath(__file__))
        image_dir=current_directory.replace('Code','')+'Media\\Images\\Logo.png'
        image=Image.open(image_dir)
        image=image.resize((450,300),Image.LANCZOS)
        photo=ImageTk.PhotoImage(image)

    except:tk.messagebox.showerror("File not found",""""It appears that the resource files have been relocated to a different folder.
Here what you can try
1.Manually move the resource files back to the Images folder.
2.Seek assistance from the back-end team (recommended).
3.If you have a copy of the original project files, consider replacing your current files with them.""")

    lb=Label(intro_window,bg='#282424',borderwidth=0)
    lb.place(x=85,y=25)

    intro_window.after(3000,lambda:xyz('Welcome to our project on',325,190,('arial',14,'bold')))
    intro_window.after(6000,lambda:xyz('Hotel Management System',355,100,('arial',24,'bold')))
    
    intro_window.after(10000,online)
    fade_in_effect(lb,image,alpha=0)
    
    intro_window.mainloop()
# This function uses a SQL query to retrieve the table names from the database
def find_table():
    global cur
    
    cur.execute("show tables where tables_in_hotelmanagement not like 'passwords'")
    table_list=[table[0] for table in cur.fetchall()]
    table_list.insert(0, ' ')
    return tuple(table_list)
#This function creates the delete window and sets up UI elements for table deletion.
def deletewindow():
    global del_table,del_window,del_pass

    try:ask_window.destroy()
    except:pass
    
    del_window=CTk.CTk();del_window.geometry("600x300+350+200");del_window.title("Delete Window");del_window.resizable(0,0)
    del_label=Label(del_window,font=('arial',12,'bold'),text="Enter your Table Name:",padx=2,bg="#282424",fg="white").grid(row=1,column=0, sticky =W)
    table_value=find_table()
    del_table=ttk.Combobox(del_window,values=table_value,state='readonly',font=('arial',12,'bold'),width=30)
    del_table.current(0)
    del_table.grid(row=1,column=1,pady=3,padx=20)

    del_pass_label=Label(del_window,font=('arial',12,'bold'),text="Enter Password:",padx=2,bg="#282424",fg="white").grid(row=2,column=0, sticky =W)
    del_pass=Entry(del_window,font=('arial',12,'bold'),width =32)
    del_pass.grid(row=2,column=1,pady=3,padx=20)
# This function retrieves the selected table name and password from the delete window.
    def delete_table():

        table_name,table_pass=str(del_table.get()),str(del_pass.get())
        tb,tup=(table_name,),(table_name,table_pass)
        if table_name==" ":tk.messagebox.showerror("No table selected","Please select a table before clicking the delete button.")
        else:
            query="select * from passwords where username=%s"
            cur.execute(query,tb)
            fetched_data=cur.fetchone()  
            if str(tup)==str(fetched_data):
                try:
                    del_table_query='drop table {tb}'.format(tb=del_table.get())    
                    cur.execute(del_table_query)
                    query='delete from passwords where username=%s'
                    cur.execute(query,(table_name,))
                    tk.messagebox.showinfo("Table Deleted","Your table has been deleted from the database.")
                    del_table.current(0)
                    del_pass.delete(0, tk.END)
                    table_value=find_table()
                    del_table.config(values=table_value)
                    con.commit()
                except:tk.messagebox.showerror("An error occurred","There was an error while deleting the table,please try again!")
            else:tk.messagebox.showerror("Incorrect Credentials","The credentials do not match our records!")

    del_btn=CTk.CTkButton(del_window,text='Delete',command=delete_table).place(x=225,y=100)
    del_btn2=CTk.CTkButton(del_window,text='Back',command=back).place(x=450,y=265)
    del_window.mainloop()
#This function filters the table values based on the user's input and updates the Combobox accordingly.
def on_combobox_keyrelease(x):
    global table_value
    
    txt=x.widget.get()
    filtered_tb=[i for i in table_value if txt.lower() in i.lower()]
    x.widget['values'] = filtered_tb
#This function creates the login window and sets up UI elements for user authentication.
def loginwindow():
    global askwin,log_window

    try:ask_window.destroy()
    except:pass

    log_window=CTk.CTk();log_window.geometry("600x300+350+200");log_window.title("Log-in Window");log_window.resizable(0,0)
    log_label=Label(log_window,font=('arial',12,'bold'),text="Enter your Hotel Name:",padx=2,bg="#282424",fg="white")
    log_label.grid(row=0,column=0,sticky=W)
    table_value=find_table()
    log_table=ttk.Combobox(log_window,values=table_value,font=('arial',12,'bold'),width=30)
    log_table.bind("<KeyRelease>",on_combobox_keyrelease)
    log_table.grid(row=0,column=1,pady=3,padx=20)
    log_pass_label=Label(log_window,font=('arial',12,'bold'),text="Enter Password:",padx=2,bg="#282424",fg="white")
    log_pass_label.grid(row=1,column=0,sticky=W)
    log_pass=Entry(log_window,font=('arial',12,'bold'),width=32)
    log_pass.grid(row=1,column=1,pady=3,padx=20)
#This function retrieves the selected table name and password from the login window.
    def login():
        global table_name
        
        try:
            table_name,table_pass=str(log_table.get()),str(log_pass.get())
            if table_name=='default_table':
                if table_pass=='':
                    log_window.destroy()
                    mainloop()
                else:raise Exception
            else:
                tb,tup=(table_name,),(table_name,table_pass)
                query="select * from passwords where username=%s"
                cur.execute(query,tb)
                fetched_data=cur.fetchone()
                if str(tup)==str(fetched_data):
                    log_window.destroy()
                    mainloop()
                else:tk.messagebox.showerror("Incorrect Credentials", "The credentials do not match our records!")
        except:tk.messagebox.showerror("Fields cannot remain empty", "You need to enter the name and the password(if required)")

    log_window.btn = CTk.CTkButton(log_window, text='Log-in', command=login).place(x=225, y=100)
    log_window.btn2 = CTk.CTkButton(log_window, text='Back', command=back).place(x=450, y=265)
    log_window.mainloop()
# This function creates the sign-in window and sets up UI elements for registering a new user.
def signinwindow():
    global ask_window,sign_window

    try:ask_window.destroy()
    except:pass
    
    sign_window=CTk.CTk();sign_window.geometry("600x300+350+200");sign_window.title("Sign-in Window");sign_window.resizable(0,0)
    sign_label=Label(sign_window,font=('arial',12,'bold'),text="Enter your Hotel Name:",padx=2,bg="#282424",fg="white").grid(row=1,column=0, sticky =W)
    sign_table=Entry(sign_window,font=('arial',12,'bold'),width =32)
    sign_table.grid(row=1,column=1,pady=3,padx=20)
    sign_pass_label=Label(sign_window,font=('arial',12,'bold'),text="Enter Password:",padx=2,bg="#282424",fg="white").grid(row=2,column=0, sticky =W)
    sign_pass=Entry(sign_window,font=('arial',12,'bold'),width =32)
    sign_pass.grid(row=2,column=1,pady=3,padx=20)
# Perform the sign-in action and register a new user.
    def sign():
        global table_name

        try:
            name=sign_table.get().replace(" ", "").strip()
            if name.isalpha():
                table_name,table_pass=sign_table.get(),sign_pass.get()
                table_name=table_name.replace(' ','_')
                if table_name=="passwords":
                    tk.messagebox.showerror("Invalid Table Name","A table with the same name already exists. Please try with another name.")
                    ask()
                else:
                        query="insert into passwords values(%s,%s)"
                        values=(table_name,table_pass)
                        cur.execute(query,values)
                        try:
                            cur.execute("""create table {tb}
                                                    (Cust_Ref_No int primary key auto_increment,Name varchar(200),Mobile bigint(20),
                                                    Type_Of_ID varchar(100),ID_No varchar(16),Check_In_Date date,Check_Out_Date date,
                                                    Room_Type varchar(100),Room_No int,No_Of_Days int,Total_Rent int)auto_increment=1""".format(tb=table_name))
                            sign_window.destroy()
                            mainloop()
                        except:tk.messagebox.showerror("Invalid Table Name","Table with the same name already exists, please try with another name.")
            else:raise IncompleteDataerror            
        except IncompleteDataerror:message=tk.messagebox.showerror("Name Missing!","The table name field cannot be left empty.")
    
    sign_window.btn1=CTk.CTkButton( sign_window, text='Sign-in',command=sign).place(x=225,y=100)
    sign_window.btn2=CTk.CTkButton( sign_window, text='Back',command=back).place(x=450,y=265)
    sign_window.mainloop()
#This function inserts the provided data into the database table.
def add_func():
    global values,table_name,rent,nod,date_1,date_2,Name_str,Name,Mobile,ID_Type,ID_No,CID,COD,Room_Type,Room_No,cur,con

    message=tk.messagebox.askyesno("Confirmation","Are you sure that you want to add the following data?")
    if message==True:
        try:
            add_query="""insert into {tb}
                    (Name,Mobile,Type_Of_ID,ID_No,Check_In_Date,Check_Out_Date,Room_Type,
                    Room_No,No_Of_Days,Total_Rent)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""".format(tb=table_name)
            cur.execute(add_query,values)
            tree.insert("",tk.END,values=(cur.lastrowid,Name_str,Mobile.get(),ID_Type.get(),ID_No.get(),CID.get(),COD.get(),Room_Type.get(),Room_No.get(),nod,rent))
            tk.messagebox.showinfo("Data Added","Following data has been added in the table.")           
            widgets=[Name, Mobile, ID_No, CID, COD]
            [i.delete(0, tk.END) for i in widgets]
            ID_Type.current(0)
            create_tooltip(ID_No,'Please select one ID Type first.')
            Room_Type.current(0)
            Room_No['value'] = ['', ]
            Room_No.current(0)
        except:tk.messagebox.showerror("An error occurred.","Something went wrong while inserting your data. Please try again.")
#This function fetches all the IDs from the table and returns a tuple with ' ' as the first element.
def id_list():
    global table_name,cur

    query='select * from {tb}'.format(tb=table_name)
    cur.execute(query)
    id_list = tuple(row[0] for row in cur.fetchall())
    id_list = (' ',) + id_list
    return id_list
# Function to handle various search operations based on search_id
def search_func():
    global search_entry_1,search_tree,search_window,search_id
# Functions to handle various search operations based on search_id
    def func():
        global e,table_name,tooltip_dict
        if search_id==1:
            try:crn=e.get()
            except:pass
            if crn==" ":
                tk.messagebox.showerror("Error","Please select a ID first!")
                search_window.lift()
            else:
                search_query='select * from {tb} where Cust_Ref_No = %s'.format(tb=table_name)
                values=(e.get(),)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.current(0)
                else:
                    tk.messagebox.showerror("Error","No matching records were found!")
                    search_window.lift()
        elif search_id==2:
            try:name=e.get()
            except:pass
            if not len(name)>=2:
                tk.messagebox.showerror("Invalid Name","Please valid name only")
                search_window.lift()
            else:
                search_query='select * from {tb} where Name=%s'.format(tb=table_name)
                values=(e.get(),)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.delete(0,'end')
                else:
                    tk.messagebox.showerror("Error","No matching records were found!")
                    search_window.lift()
        elif search_id==3:
            try:mobile=e.get()
            except:pass
            if not(mobile.isdigit() and len(mobile)==10):
                tk.messagebox.showerror("Invalid Moble No","Please enter a valid mobile number.")
                search_window.lift()
            else:
                search_query='select * from {tb} where Mobile=%s'.format(tb=table_name)
                values=(e.get(),)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.delete(0,'end')
                else:
                    tk.messagebox.showerror("Error","No matching records were found!")
                    search_window.lift()
        elif search_id==4:
            try:cid,cod=e.get(),e2.get()
            except:pass
            try:
                search_query='select * from {tb} where Check_In_Date<=%s and Check_Out_Date>=%s'.format(tb=table_name)
                values=(cod,cid)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.delete(0,'end')
                    e2.delete(0,'end')
                else:
                    tk.messagebox.showerror("Error","No matching records were found!")
                    search_window.lift()
            except:
                tk.messagebox.showerror("Invalid Date","Please enter a valid Date.")
                search_window.lift()
        elif search_id==5:
            try:
                search_query='select * from {tb} where Room_Type=%s'.format(tb=table_name)
                values=(e.get(),)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.current(0)
            except:
                    tk.messagebox.showerror("Invalid Room Type ","Please valid room type")
                    search_window.lift()
        elif search_id==6:
            try:
                search_query='select * from {tb} where Room_No=%s'.format(tb=table_name)
                values=(e.get(),)
                cur.execute(search_query,values)
                rows=cur.fetchall()
                if rows!=[]:
                    for i in rows:search_tree.insert("",tk.END,values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]))
                    e.current(0)
            except:
                    tk.messagebox.showerror("Invalid Room No","Please valid room number")
                    search_window.lift()
        else:
            tk.messagebox.showerror("Error","Please select a field!")
            search_window.lift()
# Function to handle submission of search criteria and display appropriate entry fields             
    def submit_func(event):
        global search_id,e,e2,table_name
# find table
        def find_room_no():
            cur.execute('select distinct Room_No from {t} '.format(t=table_name))
            room_no=cur.fetchall()
            tup=(' ',)
            for i in room_no:
                tup=tup+(i,)
            return tup
        
        for item  in search_tree.get_children():
            search_tree.delete(item)
        try:e.destroy()
        except:pass
        try:e2.destroy()
        except:pass
        if search_entry_1.get()==' ':pass
        elif search_entry_1.get()=='Customer Ref No':
            search_id=1
            i=id_list()
            e=ttk.Combobox(search_window,values=i,state='readonly',font=('arial',12),width=35)
            e.current(0)
            e.place(x=1000,y=245)
        elif search_entry_1.get()=='Name':
            search_id=2
            e=Entry(search_window,font=('arial',12,'bold'),width=37)
            e.place(x=1000,y=245)
        elif search_entry_1.get()=='Mobile':
            search_id=3
            e=Entry(search_window,font=('arial',12,'bold'),width=37)
            e.place(x=1000,y=245)
        elif search_entry_1.get()=='Check-in/out-Date':
            search_id=4
            e=Entry(search_window,font=('arial',12,'bold'),width=18)
            e.place(x=1000,y=245)
            e2=Entry(search_window,font=('arial',12,'bold'),width=18)
            e2.place(x=1170,y=245)
        elif search_entry_1.get()=='Room Type':
            search_id=5
            i=(' ','Superior Room with Bathtub, City Views & Twin Bed','Superior Room with Bathtub, City View & King Bed',
                  'Deluxe Room Twin Bed City View with Bathtub','Deluxe Room King Bed City View with Bathtub',
                  'Premium Room with Bathtub, Twin Bed & City View','Premium Room with Bathtub, City View & King Bed',
                  'Premium Room Airport View Twin Bed','Premium Room Airport View King Bed')
            e=ttk.Combobox(search_window,values=i,state='readonly',font=('arial',12),width=35)
            e.current(0)
            e.place(x=1000,y=245)
        elif search_entry_1.get()=='Room No':
            search_id=6
            i=find_room_no()
            e=ttk.Combobox(search_window,values=i,state='readonly',font=('arial',12),width=35)
            e.current(0)
            e.place(x=1000,y=245)
        
    search_window=CTk.CTk();search_window.title("Search Window");search_window.geometry('1360x450+0+100');search_window.resizable(0,0)

    xyz=(' ','Customer Ref No','Name','Mobile','Check-in/out-Date','Room Type','Room No')
    search_label=Label(search_window,font=('arial',12,'bold'),text="Enter the Customor Reference No:",bg="#282424",fg="white").grid(row=10,column=0,sticky=W)
    search_entry_1=ttk.Combobox(search_window,values=xyz,state='readonly',font=('arial',12),width=18)
    search_entry_1.current(0)
    search_entry_1.bind("<<ComboboxSelected>>",submit_func)
    search_entry_1.place(x=800,y=245)

    search_window.txtspace=Text(search_window,height=15,width=110,font=('arial',11,'bold'))
    search_window.txtspace.grid(row=1,column=0,columnspan=2,padx=2,pady=5)

    columns = [('Cust. Ref. No.', 100, 100),('Name', 200, 200),('Mobile', 75, 75),('Type of ID', 100, 100),('ID No', 100, 100),('Check In Date', 100, 100),
               ('Check Out Date', 100, 100),('Room Type', 310, 310),('Room No', 75, 75),('No of Days', 75, 75),('Rent', 100, 100)]
    headings = ['Cust. Ref. No.', 'Name', 'Mobile', 'Type of ID', 'ID No', 'Check In Date', 'Check Out Date', 'Room Type', 'Room No', 'No Of Days', 'Total Rent']

    search_tree = ttk.Treeview(search_window.txtspace, show='headings', columns=[col[0] for col in columns])
    [search_tree.column(col, width=width, minwidth=minwidth, anchor=tk.CENTER) for col, width, minwidth in columns]
    [search_tree.heading(col[0], text=heading) for col, heading in zip(columns, headings)]
    search_tree.pack()
    
    search_window.btnSearch=CTk.CTkButton( search_window, font=('arial',20,'bold'),text="Search", command=func).place(x=550,y=300)

    scroll=ttk.Scrollbar(search_window,orient='vertical')
    scroll.configure(command=tree.yview)
    search_tree.configure(yscrollcommand=scroll.set)
    scroll.place(x=1340,y=5,height=231)

    search_window.mainloop()
# Function to retrieve data from the database and insert it into the Treeview widget for display
def insert():
    global tree,table_name,cur
    
    cur.execute('select * from {tb}'.format(tb=table_name))
    rows=cur.fetchall()
    [tree.insert("", 'end', values=row) for row in rows]
# Function to clear all data from the table and Treeview widget

def clear_func():
    global table_name,tree
    
    message=tk.messagebox.askyesno("Confirmation Message","Do you really want to clear all of the data of your table")
    if message==True:
        for item in tree.get_children():
            tree.delete(item)
        cur.execute("delete from {tb}".format(tb=table_name))
        tk.messagebox.showinfo("Data Cleared","All of the data from your table has been deleted.")
# Function to delete selected data from the table
def delete_func():
    global table_name,cur,con

    try:
        item=tree.selection()[0]
        User_ID=tree.item(item)['values'][0]
        ask=tk.messagebox.askyesno("Hotel Management System",
                                   "Do you really want to delete the following data?")
        if ask==True:
            delete='delete from {tb} where Cust_Ref_No=%s'.format(tb=table_name)
            rows=(User_ID,)
            cur.execute(delete,rows)
            tree.delete(item)
            tk.messagebox.showinfo("Data Deleted","Following data has been deleted from the table.")
        else:
            pass
    except:
        tk.messagebox.showerror('Error Occured','Please select a row first, before clicking "Delete" button.')
# Function to confirm and handle program exit
def exit_func():
    global window,search_window,con,update_window,update_win_1
    
    exit_message=tk.messagebox.askyesnocancel("Hotel Management System","Confirm,if you want to exit")
    if exit_message==True:
        try:search_window.destroy()
        except:pass
        try:update_window.destroy()
        except:pass
        try:update_win_1.destroy()
        except:pass
        window.destroy()
        con.commit()
        ask()
    elif exit_message==False:
        try:search_window.destroy()
        except:pass
        try:update_window.destroy()
        except:pass
        try:update_win_1.destroy()
        except:pass
        window.destroy()
        con.rollback()
        ask()
    else:pass
# Function to format dates to 'YYYY-MM-DD' format recursively
def format_dates(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, list):
        return [format_dates(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(format_dates(item) for item in obj)
    elif isinstance(obj, dict):
        return {key: format_dates(value) for key, value in obj.items()}
    else:
        return obj
# Close update window and call update function
def update_back():
    global update_win_1

    update_win_1.destroy()
    update_func()
# Update the displayed values of the selected row in the treeview with the latest database values
def tree_update():
    global user_id
    
    cur.execute('select * from {tb} where Cust_Ref_No={uid}'.format(tb=table_name,uid=user_id))
    tup=cur.fetchall()
    tup=tup[0]
    tup=format_dates(tup)
    tup=(str(tup[0]),tup[1],str(tup[2]),tup[3],tup[4],tup[5],tup[6],tup[7],str(tup[8]),str(tup[9]),str(tup[10]))
    uid=tree.selection()
    uid=uid[0]
    tree.item(uid,values=tup)
 # Create a window to update the name   
def update_Name():
    global update_window,update_win_1,tooltip_dict

    update_win_1=CTk.CTk();update_win_1.title("Update Window");update_win_1.geometry('600x250+300+200');update_win_1.resizable(0,0)
    
    label=Label(update_win_1,font=('arial',12,'bold'),text="Enter the name: ",padx=2,pady=2,bg="#282424",fg="white")
    label.grid(row=1,column=0,sticky=W)
    entry1=Entry(update_win_1,font=('arial',12,'bold'),width =37)
    entry1.grid(row=1,column=1,pady=3,padx=20)
    create_tooltip(entry1,tooltip_dict['Name'])
# Update the name in the database for the given customer reference number
    def update():
        global user_id,table_name,cur,con,tree
        
        value=str(entry1.get())
        value_str=value.replace(' ','')
        if not value_str.isalpha() or len(value_str)<2:
            tk.messagebox.showerror("Invalid Name",
                                    "The name should contain only letters and spaces; a minimum of two letters is required. Please try again. ")
            update_win_1.lift()
        else:
            try:
                value=value.title()
                query='update {a} set Name=%s where Cust_Ref_No={c}'.format(a=table_name,c=user_id)
                cur.execute(query,(value,))
                tree_update()
                tk.messagebox.showinfo("Name Updated","Name of the booking with Cust_Ref_No ({uid})has been updated in the table.".format(uid=user_id))
                update_win_1.destroy()
                update_func()
            except FileExistsError:
                tk.messagebox.showerror("Error Occured!","An error occurred while attempting to update the name in our database. Please try the update again.")
                update_win_1.lift()
                
    update_win_1.btn=CTk.CTkButton(update_win_1, text="Update", command=update).place(x=225,y=100)
    update_win_1.btn2=CTk.CTkButton(update_win_1, text="Back", command=update_back,width=75).place(x=522,y=216)
        
    update_win_1.mainloop()
# Create a window to update the mobile number
def update_Mobile():
    global update_window,update_win_1,tooltip_dict

    update_win_1=CTk.CTk();update_win_1.title("Update Window");update_win_1.geometry('600x250+300+200');update_win_1.resizable(0,0)
    
    label=Label(update_win_1,font=('arial',12,'bold'),text="Enter the Mobile No. : ",padx=2,pady=2,bg="#282424",fg="white")
    label.grid(row=1,column=0,sticky=W)
    entry1=Entry(update_win_1,font=('arial',12,'bold'),width =37)
    entry1.grid(row=1,column=1,pady=3,padx=20)
    create_tooltip(entry1,tooltip_dict['Mobile'])
 # Update the mobile number in the database   
    def update():
        global user_id,table_name,cur,con,uid

        uid=user_id
        value=str(entry1.get())
        
        if value.isdigit() and len(value)==10:
            try:
                query='update {a} set Mobile=%s where Cust_Ref_No={c}'.format(a=table_name,c=user_id)
                cur.execute(query,(value,))
                tree_update()
                tk.messagebox.showinfo("Mobile No. Updated","Mobile No. of the booking with Cust_Ref_No ({uid})has been updated in the table.".format(uid=user_id))
                update_win_1.destroy()
                update_func()
            except:
                tk.messagebox.showerror("Error Occured!","An error occurred while attempting to update the Mobile No. in our database. Please try the update again.")
                update_win_1.lift()
        else:
            tk.messagebox.showerror("Invalid Mobile No.",
                                    "The 'Mobile No.' field should only contain digits and must have exactly 10 digits. Please ensure the input meets this requirement.")
            update_win_1.lift()
            
    update_win_1.btn=CTk.CTkButton(update_win_1, text="Update", command=update).place(x=250,y=100)
    update_win_1.btn2=CTk.CTkButton(update_win_1, text="Back", command=update_back,width=75).place(x=522,y=216)
    
    update_win_1.mainloop()
# Function to update the ID goes here
def update_ID():
    global update_window,update_win_1,tooltip_dict
# This function handles the event when the user selects an ID type from the combobox.
# It sets a tooltip based on the selected ID type.

    def tip_func(event):
        value=update_ID_Type.get()
        if value=='Aadhar Card':
            create_tooltip(entry1,tooltip_dict['Aadhar'])
        elif value=='Driving Licence':
            create_tooltip(entry1,tooltip_dict['Driving'])
        elif value=='Passport':
            create_tooltip(entry1,tooltip_dict['Passport'])
        else:create_tooltip(entry1,'Please select one ID Type first.')
        
    update_win_1=CTk.CTk()
    update_win_1.title("Update Window")
    update_win_1.geometry('600x250+300+200')
    update_win_1.resizable(0,0)

    label=Label(update_win_1,font=('arial',12,'bold'),text="Enter the ID type: ",padx=2,pady=2,bg="#282424",fg="white")
    label.grid(row=0,column=0,sticky=W)
    update_ID_Type=ttk.Combobox(update_win_1,state='readonly',font=('arial',12,'bold'),width=35)
    update_ID_Type['value']=(' ','Aadhar Card','Driving Licence','Passport')
    update_ID_Type.current(0)
    update_ID_Type.bind("<<ComboboxSelected>>",tip_func)
    update_ID_Type.grid(row=0,column=1,pady=3,padx=20)
    create_tooltip(update_ID_Type,tooltip_dict['ID_Type'])
    
    label=Label(update_win_1,font=('arial',12,'bold'),text="Enter the ID No. : ",padx=2,pady=2,bg="#282424",fg="white")
    label.grid(row=1,column=0,sticky=W)
    entry1=Entry(update_win_1,font=('arial',12,'bold'),width =37)
    entry1.grid(row=1,column=1,pady=3,padx=20)
    create_tooltip(entry1,'Please select an ID type.')
# This function handles the process of updating the ID information for a customer.    
    def update():
        global user_id,table_name,cur,con,uid

        uid=user_id
        value2=str(entry1.get())
        value=str(update_ID_Type.get())
        
        try:
            if value=='Aadhar Card':
                if len(value2)!=12 or not value2.isdigit():
                    tk.messagebox.showerror("Incorrect Format",
                                                   """The Aadhaar Number should consist of 12 digits. Please enter the correct 12-digit Aadhaar Number.""")
                    raise IDException
            elif value=='Driving Licence':
                value2=value2.replace(' ', '-')
                pattern=r'^[A-Za-z]{2}-\d{13}$'
                if not re.match(pattern,value2):
                    tk.messagebox.showerror("Incorrect Format",
                                                    """The driving license format is as follows: the first two characters should be alphabets, followed by a hyphen ('-'), and then the remaining 13 characters should be digits (numbers). Please provide the driving license number in this correct format.""")
                    raise IDException
            elif value=='Passport':
                pattern = r'^[A-Z][1-9][0-9]{2}[0-9]{4}$'
                if not re.match(pattern,value2):
                    tk.messagebox.showerror("Incorrect Format",
                                                    """The valid Indian passport number should be 8 characters long. The first character should be an uppercase alphabet, the next two characters should follow the pattern: the first being a number from 1 to 9, and the second being any number from 0 to 9. The remaining four characters can be any combination of digits (numbers from 0 to 9). Please enter the passport number in this correct format.""")
                    raise IDException
            try:
                query='update {a} set ID_No=%s,Type_Of_ID=%s where Cust_Ref_No={c}'.format(a=table_name,c=user_id)
                cur.execute(query,(value2,value))
                tree_update()
                tk.messagebox.showinfo("ID Updated","ID of the booking with Cust_Ref_No ({uid})has been updated in the table.".format(uid=user_id))
                update_win_1.destroy()
                update_func()
            except:
                tk.messagebox.showerror("Error Occured!","There was an error encountered while attempting to update the Mobile No. in our database. Please retry the update.")
                update_win_1.lift()
        except IDException:update_win_1.lift()
                
    update_win_1.btn=CTk.CTkButton(update_win_1, text="Update", command=update).place(x=250,y=100)
    update_win_1.btn2=CTk.CTkButton(update_win_1, text="Back", command=update_back,width=75).place(x=522,y=216)
    
    update_win_1.mainloop()
# This function sets up the update window for modifying check-in and check-out dates.

def update_CIOD():
    global update_window,update_win_1,tooltip_dict

    update_win_1=CTk.CTk();update_win_1.title("Update Window");update_win_1.geometry('600x250+300+200');update_win_1.resizable(0,0)
    
    label=Label(update_win_1,font=('arial',12,'bold'),text="Enter the Check-in-Date: ",padx=2,pady=2,bg="#282424",fg="white")
    label.grid(row=1,column=0,sticky=W)
    entry1=Entry(update_win_1,font=('arial',12,'bold'),width =37)
    entry1.grid(row=1,column=1,pady=3,padx=20)
    create_tooltip(entry1,tooltip_dict['Check-in-Date'])

    label2=Label(update_win_1,font=('arial',12,'bold'),text="Enter the Check-out-Date: ",padx=2,pady=2,bg="#282424",fg="white")
    label2.grid(row=2,column=0,sticky=W)
    entry2=Entry(update_win_1,font=('arial',12,'bold'),width =37)
    entry2.grid(row=2,column=1,pady=3,padx=20)
    create_tooltip(entry2,tooltip_dict['Check-out-Date'])
# This function handles the process of updating the check-in and check-out dates for a customer's booking.

    def update():
        global user_id,table_name,cur,con,uid

        uid=user_id
        value,value2=str(entry1.get()),str(entry2.get())
        value=value.replace('/','-')
        value2=value2.replace('/','-')
        
        year_1,year_2=int(value[0:4]),int(value2[0:4])
        month_1,month_2=int(value[5:7]),int(value2[5:7])
        day_1,day_2=int(value[8:10]),int(value2[8:10])

        a,b=value.replace(" ",""),value2.replace(" ","")
        if a=="":
            tk.messagebox.showerror("Field cannot  be empty","The entry box must be filled. Please enter your ID No.")
            update_win_1.lift()
        elif b=="":
            tk.messagebox.showerror("Field can't be empty","The entry box must be filled. Please enter your ID Type.")
            update_win_1.lift()
        else:
            try:
                query='select Room_No,Room_Type from {} where Cust_Ref_No={}'.format(table_name,uid)
                cur.execute(query)
                room_str=cur.fetchall()
                room=room_str[0][0]
                
                QUERY = "SELECT * FROM {} WHERE Room_No = %s AND Check_In_Date <= %s AND Check_Out_Date >= %s".format(table_name)
                values = (room, value2, value)
                cur.execute(QUERY, values)
                x=cur.fetchall()
                if x!=[]:raise RoomBookederror
                try:
                    date_1,date_2=datetime.date(year_1,month_1,day_1),datetime.date(year_2,month_2,day_2)
                    try:
                        if date_1>=date_2:raise Dateerror
                        else:
                            nod=int(day_2-day_1)
                            nod_tuple=(nod,)
                            rent=rent_func(room_str[0][1])
                            rent=rent*nod

                            query='''update {a} set Check_In_Date=%s,Check_Out_Date=%s,Total_Rent={r} where Cust_Ref_No={c}'''.format(a=table_name,r=rent,c=user_id)
                            cur.execute(query,(value,value2))
                            tree_update()
                            tk.messagebox.showinfo("Check-In/Out-Date Updated",
                                                                "Check-In/Out-Date of the booking with Cust_Ref_No ({uid})has been updated in the table.".format(uid=user_id))
                            update_win_1.destroy()
                            update_func()
                    except Dateerror:
                            tk.messagebox.showerror("Typing Error","The check-in date cannot be after the check-out date.")
                            update_win_1.lift()
                except ValueError:
                    tk.messagebox.showerror("Invalid Date!","Please enter a date in a valid format.")
                    update_win_1.lift()
            except RoomBookederror:
                tk.messagebox.showerror("Room Already Booked","The room has already been booked by someone else. Please try selecting different dates or choose a different room.")
                update_win_1.lift()

    update_win_1.btn=CTk.CTkButton(update_win_1, text="Update", command=update).place(x=250,y=100)
    update_win_1.btn2=CTk.CTkButton(update_win_1, text="Back", command=update_back,width=75).place(x=522,y=216)
    
    update_win_1.mainloop()
# This function updates the available room numbers in a combobox based on the selected room type.
def update_rooms_list_2(x):
    global Room_No,room_no_dict,update_win_1_Room_Type
    
    selected_type=update_win_1_Room_Type.get()
    if selected_type in room_no_dict:
        Room_No_update['values']=room_no_dict[selected_type]
    else:
        Room_No_update['values']=['',]
# This function sets up the update window for modifying the room type and room number for a booking.
def update_Room():
    global update_window,update_win_1,Room_No_update,selected_number,update_win_1_Room_Type,tooltip_dict

    selected_type=tk.StringVar()
    selected_number=tk.StringVar()

    update_win_1=CTk.CTk()
    update_win_1.title("Update Window")
    update_win_1.geometry('600x250+300+200')
    update_win_1.resizable(0,0)
    
    windowlabel_1=Label(update_win_1,font=("arial",12,'bold'),text="Room Type:",padx=2,pady=2,bg="#282424",fg="white")
    windowlabel_1.grid(row=8,column=0,sticky=W)
    update_win_1_Room_Type=ttk.Combobox(update_win_1,textvariable=selected_type,state='readonly',font=('arial',12,'bold'),width=35)
    update_win_1_Room_Type['value']=room_type_list
    update_win_1_Room_Type.current(0)
    update_win_1_Room_Type.grid(row=8,column=1,pady=3,padx=20)
    update_win_1_Room_Type.bind("<<ComboboxSelected>>", update_rooms_list_2)
    create_tooltip(update_win_1_Room_Type,tooltip_dict['Room_Type'])

    windowlabel_2=Label(update_win_1,font=('arial',12,'bold'),text="Room No: ",padx=2,pady=2,bg="#282424",fg="white")
    windowlabel_2.grid(row=9,column=0,sticky=W)
    Room_No_update=ttk.Combobox(update_win_1,textvariable=selected_number,state="readonly",font=('arial',12,'bold'),width=35)
    Room_No_update['value']=['',]
    Room_No_update.current(0)
    Room_No_update.grid(row=9,column=1,pady=3,padx=20)
    create_tooltip(Room_No_update,tooltip_dict['Room_No'])
# This function handles the process of updating the room type and room number for a customer's booking.

    def update():
        global user_id,table_name,cur,con,uid

        uid=user_id
        value=str(update_win_1_Room_Type.get())
        value2=str(Room_No_update.get())
        if value==" " or value2==" ":
            message=tk.messagebox.showerror("Field can't be empty",
                                                 "The entry box must be filled. Please enter your ID No.")
            update_win_1.lift()
        else:
            query="select Check_In_Date,Check_Out_Date from {tb} where Cust_Ref_No={i}".format(tb=table_name,i=int(uid))
            cur.execute(query)
            dates=cur.fetchall()
            
            date_tuple=(dates[0][0],dates[0][1])
            date_strings=[date.strftime('%Y-%m-%d') for date in date_tuple]
            cid,cod=date_strings[0],date_strings[1]
            day1,day2=cid.split('-')[2],cod.split('-')[2]
            nod=int(day2)-int(day1)
            try:            
                QUERY="SELECT * FROM {} WHERE Room_No = %s AND Check_In_Date <= %s AND Check_Out_Date >= %s".format(table_name)
                values=(value2,cod,cid)
                cur.execute(QUERY, values)
                room=cur.fetchall()
                if room!=[]:
                    raise Exception
                else:
                    rent=rent_func(value)
                    z=rent*nod
                    
                    query='''update {a} set Room_Type=%s,Room_No=%s,Total_Rent=%s where Cust_Ref_No={c}'''.format(a=table_name,c=user_id)
                    cur.execute(query,(value,value2,z))
                    tree_update()
                    tk.messagebox.showinfo("Check-In/Out-Date Updated",
                                                        "Check-In/Out-Date of the booking with Cust_Ref_No ({uid})has been updated in the table.".format(uid=user_id))
                    update_win_1.destroy()
                    update_func()
            except:
                tk.messagebox.showerror("Room Already Booked","The room has already been booked by someone else. Please try selecting different dates or choose a different room.")
                update_win_1.lift()
                
    update_win_1.btn=CTk.CTkButton(update_win_1, text="Update", command=update).place(x=250,y=100)
    update_win_1.btn2=CTk.CTkButton(update_win_1, text="Back", command=update_back,width=75).place(x=522,y=216)
    
    update_win_1.mainloop()
# This function determines which update function to call based on the selected field from the dropdown menu.    
def update_assign_func():
    global entry,update_window

    e=entry.get()
    update_window.destroy()
    
    if e=='Name':update_Name()
    elif e=='Mobile':update_Mobile()
    elif e=='ID Type/ID No':update_ID()
    elif e=='Check In/Out Date':update_CIOD()
    elif e=='Room':update_Room()
    else:
        tk.messagebox.showerror("Fill the entry box","The entry box must be filled. Please select one field from the drop-down menu.")
        update_func()
# This function sets up a window to choose the field for updating and calls the appropriate update function.

def update_func():
    global update_window,entry,user_id,uid
    
    try:
        try:
            item=tree.focus()
            values=tree.item(item,'values')
            user_id=values[0]
        except:user_id=uid
        
        update_window=CTk.CTk();update_window.title("Update Window");update_window.geometry('500x250+400+200');update_window.resizable(0,0)
        
        label=Label(update_window,font=('arial',12,'bold'),text="What do you want to update: ",padx=2,pady=2,bg="#282424",fg="white")
        label.grid(row=4,column=0,sticky=W)
        entry=ttk.Combobox(update_window,state='readonly',font=('arial',12,'bold'),width=18)
        entry['value']=(' ','Name','Mobile','ID Type/ID No','Check In/Out Date','Room')
        entry.current(0)
        entry.grid(row=4,column=1,pady=3,padx=20)

        update_window.btn=CTk.CTkButton(update_window,text="Continue", command=update_assign_func).place(x=175,y=100)

        update_window.mainloop()
    except:tk.messagebox.showerror('Error Occured','Please select a row before clicking the "Update" button.')
# This function validates the entered data for adding a customer's booking and performs necessary checks.

def check():
    global table_name,values,rent,nod,cur,date_1,date_2,Name_str,Name,Mobile,ID_Type,ID_No,CID,COD,Room_Type,Room_No,room_dict

    try:
        values=(Name.get(),Mobile.get(),ID_Type.get(),ID_No.get(),CID.get(),COD.get(),Room_Type.get(),Room_No.get())
        for i in values:
            if i=='' or i==' ':
                raise IncompleteDataerror()

        Mob_str=str(Mobile.get())
        ID_No_str=str(ID_No.get())
        ID_Type_str=str(ID_Type.get())
        Name_str=str(Name.get())
        Name_str=Name_str.replace(" ","")
        
        if not Name_str.isalpha() or len(Name_str)<2:
            message=tk.messagebox.showerror("The name provided is too short",
                                            """The name should consist of at least 2 letters and only contain alphabets and spaces. Please enter a valid name. """)
            raise IDException
        elif len(Mobile.get())!=10 or not Mob_str.isdigit():
            tk.messagebox.showerror("Invalid Mobile No.",
                                    "The 'Mobile No.' field should only contain digits, and the number of digits must be exactly 10. Please ensure the input meets this requirement.")
            raise IDException
        elif ID_Type_str=='Aadhar Card':
            if len(ID_No_str)!=12 or not ID_No_str.isdigit:
                tk.messagebox.showerror("Incorrect Format",
                                               """The Aadhaar Number should consist of 12 digits. Please enter the correct 12-digit Aadhaar Number.""")
                raise IDException
        elif ID_Type_str=='Driving Licence':
            ID_No_str=ID_No_str.replace(' ', '-')
            pattern=r'^[A-Za-z]{2}-\d{13}$'
            if not re.match(pattern,ID_No_str):
               tk.messagebox.showerror("Incorrect Format",
                               """The driving license format should have the first two characters as alphabets, followed by a hyphen ('-'), and then the remaining 13 characters should be digits (numbers). Please provide the driving license number in this correct format.""")
               raise IDException
        elif ID_Type_str=='Passport':
            pattern = r'^[A-Z][1-9][0-9]{2}[0-9]{4}$'
            if not re.match(pattern,ID_No_str):
                tk.messagebox.showerror("Incorrect Format",
                               """The valid Indian passport number should be 8 characters long. The first character should be an uppercase alphabet, followed by two characters where the first must be a number from 1 to 9 and the second can be any number from 0 to 9. The remaining four characters can be any combination of digits (numbers from 0 to 9). Please enter the passport number in this correct format.""")
                raise IDException

        no,Name_str=Room_No.get(),Name.get()
        Name_str=Name_str.title()
        values=(Name_str,Mobile.get(),ID_Type.get(),ID_No.get(),CID.get(),COD.get(),Room_Type.get(),Room_No.get())
        
        try:
            cid,cod=str(CID.get()),str(COD.get())
            year_1,year_2=int(cid[0:4]),int(cod[0:4])
            month_1,month_2=int(cid[5:7]),int(cod[5:7])
            day_1,day_2=int(cid[8:10]),int(cod[8:10])
            date_1,date_2=datetime.date(year_1,month_1,day_1),datetime.date(year_2,month_2,day_2)
            if date_1>=date_2:raise Dateerror("Please check your check-in/check-out date!")

            nod=int(day_2-day_1)
            nod_tuple=(nod,)
            room=Room_Type.get()
            rent=rent_func(room)
            rent=rent*nod
            rent_tuple=(rent,)

            values=values+nod_tuple+rent_tuple
            
            QUERY="select * from {tb} where Room_No={n} and Check_In_Date<='{d}' and Check_Out_Date>='{d2}'".format(tb=table_name,n=no,d=cod,d2=cid)
            cur.execute(QUERY)
            rooms_booked=cur.fetchall()
            if rooms_booked==[]:add_func()
            else:raise RoomBookederror
        except ValueError:tk.messagebox.showerror("Invalid Date!","Please enter a valid date!")    
    except Dateerror:
        tk.messagebox.showerror("Typing Error","The Check-in-date can't fall after Check-out-date.")
    except IncompleteDataerror:
        tk.messagebox.showerror("Missing Data","Please fill all of the fields.")
    except RoomBookederror:
        tk.messagebox.showerror("Room Already Booked","The room has been already booked by someone else, try changing dates or room.")
    except IDException:pass
# This function updates the available room numbers in a combobox based on the selected room type.
def update_rooms_list(x):
    global selected_room_type,Room_No,room_no_dict
    
    selected_type=selected_room_type.get()
    if selected_type in room_no_dict:Room_No['values']=room_no_dict[selected_type]
    else:Room_No['values']=['',]
# This function creates a tooltip for a given widget with the specified tooltip text.
def create_tooltip(widget, tooltip_text):
    global window,update_win_1

    try:
        tooltip=Pmw.Balloon(window)
        tooltip.bind(widget, tooltip_text)
    except:
        tooltip=Pmw.Balloon(update_win_1)
        tooltip.bind(widget, tooltip_text)
# Initialize and configure the main application window.
# Create various GUI elements like labels, entries, comboboxes, buttons, etc.
# Configure event bindings for combobox selections.
# Set up a Treeview for displaying data in a tabular format.
# Pack and display the GUI components within the main window.

def mainloop():
    try:
        global cur,con,tree,window_txt_space,Name,Mobile,ID_Type,ID_No,CID,COD,selected_room_type,tree
        global Room_Type,Room_No,window,table_name,room_type_list,selected_room_number,tree,tooltip_dict

        def close_window():
            pass
    # Check the selected ID Type and create a tooltip accordingly.
    # Attach the tooltip to the appropriate entry field.
        def tip_func(event):
            value=ID_Type.get()
            if value=='Aadhar Card':
                create_tooltip(ID_No,tooltip_dict['Aadhar'])
            elif value=='Driving Licence':
                create_tooltip(ID_No,tooltip_dict['Driving'])
            elif value=='Passport':
                create_tooltip(ID_No,tooltip_dict['Passport'])
            else:create_tooltip(ID_No,'Please select one ID Type first.')
        
        window=CTk.CTk();window.geometry("{}x{}+0+0". format(window.winfo_screenwidth(), window.winfo_screenheight()))
        window.after(500,)
        window.title(str(table_name)+"'s Database")
        window.protocol("WM_DELETE_WINDOW",close_window)

        current_directory=os.path.dirname(os.path.abspath(__file__))
        video_dir=current_directory.replace('Code','')+'Media\\Videos\\Main_Video.mp4'
        
        video_label=Label(window,bg="#282424")
        video_label.place(x=800, y=285)
  
        cap=cv2.VideoCapture(video_dir)
        photo=None
        def update():
            ret, frame=cap.read()
            if ret:
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame=cv2.resize(frame, (500,300))
                photo=ImageTk.PhotoImage(image=Image.fromarray(frame))
                video_label.config(image=photo)
                video_label.photo=photo
                window.after(7, update)  
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
                update() 
        update()
        
        selected_room_type,selected_room_number=tk.StringVar(),tk.StringVar()
        
        cur.execute('select * from {tb};'.format(tb=table_name))
        rows=cur.fetchall()

        windowlabel_1=Label(window, font=('arial',12,'bold'),text="Name:",padx=2,bg="#282424",fg="white").grid(row=2,column=0,sticky=W)
        Name=Entry(window, font=('arial',12,'bold'),width =37)
        Name.grid(row=2,column=0,pady=3,padx=20)
        create_tooltip(Name,tooltip_dict['Name'])

        windowlabel_2=Label(window,font=('arial',12,'bold'),text="Mobile:",padx=2,pady=2,bg="#282424",fg="white").grid(row=3, column=0, sticky=W)
        Mobile=Entry(window,font=('arial',12,'bold'),width=37)
        Mobile.grid(row=3,column=0,pady=3,padx=20)
        create_tooltip(Mobile,tooltip_dict['Mobile'])

        windowlabel_3=Label(window,font=('arial',12,'bold'),text="Type of ID:",padx=2,pady=2,bg="#282424",fg="white").grid(row=4,column=0,sticky=W)
        ID_Type=ttk.Combobox(window,state='readonly',font=('arial',12,'bold'),width=35)
        ID_Type['value']=(' ','Aadhar Card','Driving Licence','Passport')
        ID_Type.current(0)
        ID_Type.bind("<<ComboboxSelected>>",tip_func)
        ID_Type.grid(row=4,column=0,pady=3,padx=20)
        create_tooltip(ID_Type,tooltip_dict['ID_Type'])
        
        windowlabel_4=Label(window,font=('arial',12,'bold'),text="ID No:",padx=2,bg="#282424",fg="white").grid(row=5,column=0, sticky =W)
        ID_No=Entry(window,font=('arial',12,'bold'),width =37)
        ID_No.grid(row=5,column=0,pady=3,padx=20)
        create_tooltip(ID_No,'Please select one ID Type first.')
        
        windowlabel_5=Label(window,font=('arial',12,'bold'),text="Check In Date:",padx=2,pady=2,bg="#282424",fg="white").grid(row=6,column=0,sticky=W)
        CID=Entry(window,font=('arial',12,'bold'),width=37)
        CID.grid(row=6,column=0,pady=3,padx=20)
        create_tooltip(CID,tooltip_dict['Check-in-Date'])

        windowlabel_6=Label(window,font=('arial',12,'bold'),text="Check Out Date:",padx=2,pady=2,bg="#282424",fg="white").grid(row=7,column=0,sticky=W)
        COD=Entry(window,font=('arial',12,'bold'),width=37)
        COD.grid(row=7,column=0,pady=3,padx=20)
        create_tooltip(COD,tooltip_dict['Check-out-Date'])
        
        windowlabel_7=Label(window,font=("arial",12,'bold'),text="Room Type:",padx=2,pady=2,bg="#282424",fg="white")
        windowlabel_7.grid(row=8,column=0,sticky=W)
        Room_Type=ttk.Combobox(window,textvariable=selected_room_type,state='readonly',font=('arial',12,'bold'),width=35)
        Room_Type['value']=room_type_list
        Room_Type.current(0)
        Room_Type.grid(row=8,column=0,pady=3,padx=20)
        Room_Type.bind("<<ComboboxSelected>>", update_rooms_list)
        create_tooltip(Room_Type,tooltip_dict['Room_Type'])
        
        windowlabel_8=Label(window,font=('arial',12,'bold'),text="Room No: ",padx=2,pady=2,bg="#282424",fg="white").grid(row=9,column=0,sticky=W)
        Room_No=ttk.Combobox(window,textvariable=selected_room_number,state="readonly",font=('arial',12,'bold'),width=35)
        Room_No['value']=['',]
        Room_No.current(0)
        Room_No.grid(row=9,column=0,pady=3,padx=20)
        create_tooltip(Room_No,tooltip_dict['Room_No'])
        
        window.btn=CTk.CTkButton( window, font=('arial',20,'bold'),text="Check Availability", command=check).place(x=265,y=560)
        
        window_txt_space=Text(window,height=15,width=110,font=('arial',11,'bold'))
        window_txt_space.grid(row=1,column=0,columnspan=2,padx=2,pady=20)

        tree=ttk.Treeview(window_txt_space, columns=('Cust. Ref. No.', 'Name', 'Mobile', 'Type of ID', 'ID No', 'Check In Date',
                                                       'Check Out Date', 'Room Type', 'Room No', 'No of Days', 'Rent'), show='headings')
        column_widths = {'Cust. Ref. No.': 100, 'Name': 190, 'Mobile': 75, 'Type of ID': 100, 'ID No': 110, 'Check In Date': 100,
                         'Check Out Date': 100, 'Room Type': 310, 'Room No': 75, 'No of Days': 75, 'Rent': 100}
        for col, width in column_widths.items():
            tree.column(col, width=width, minwidth=width, anchor=tk.CENTER)
            tree.heading(col, text=col)

        scroll=ttk.Scrollbar(window_txt_space,orient='vertical')
        scroll.configure(command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT,fill=Y)

        tree.pack()
        insert()
        
        canvas=tk.Canvas(window,width=3000,height=(-10)).place(x=0,y=625)
        
        window.btnSearch=CTk.CTkButton( window, font=('arial',20,'bold'), text="Search", command=search_func).place(x=90,y=660)
        window.btnUpdate=CTk.CTkButton( window, font=('arial',20,'bold'), text="Update", command=update_func).place(x=340,y=660)
        window.btnDelete=CTk.CTkButton( window, font=('arial',20,'bold'), text="Delete", command=delete_func).place(x=590,y=660)
        window.btnClear=CTk.CTkButton( window, font=('arial',20,'bold'), text="Clear", command=clear_func).place(x=840,y=660)
        window.btnExit=CTk.CTkButton( window, font=('arial',20,'bold'), text="Exit", command=exit_func).place(x=1090,y=660)

        window.mainloop()
    except Exception as e:print(e)
# Function to handle online database connectivity.        
def online():
    global cur,con,n

    try:
        n=1
        con=mc.connect(host="mysql-1a1d8a65-kentoarai002-0e8b.a.aivencloud.com",user='avnadmin',password="AVNS_S0NuxGvID7J52Z0tf-i",port=24000)
        cur=con.cursor()
        cur.execute('use hotelmanagement')
        cur.execute("create table if not exists passwords(username varchar(200) primary key,password varchar(100))")
        cur.execute("set autocommit=OFF")
        ask()
    except Exception as e:
        print(e)
        tk.messagebox.showerror("Something went wrong",
                                           """An error occurred while attempting to connect to the remote server. Please follow these steps to troubleshoot the issue:
1.Check your internet connection and ensure it is stable. Retry the connection after ensuring a stable internet connection.
2.Wait for some time and try the connection again. There might be a temporary issue with our remote server.
3.If the issue persists, feel free to contact our support team. Our dedicated team will do their best to assist you and resolve the problem.""")        
        offline()
# Function to handle offline mode or local database usage.    
def offline():
    global local_password,local_user,local_user_lb,local_pass_lb
# Function to handle user events or actions.
    def user(event):
        global e1,txt_btn1,user,local_label_1,local_file_dir,off_win

        def work():
            file=open(local_file_dir,'r')
            cred=file.read()
            cred=cred.split('#')
            file.close()

            data=str(user)+'#'+str(cred[1])
            
            file=open(local_file_dir,'w')
            file.write(data)
            file.close()
            
        user=e1.get()
        e1.destroy()
        txt_btn1.destroy()

        if user=="":
            local_label_1.configure(text="Empty")
            work()
        elif user.isspace():tk.messagebox.showerror('Error',"A MySQL username that contains only spaces is not allowed. Please provide a username that includes at least one non-space character.")
        else:
            local_label_1.configure(text=user)
            work()
# Function to handle events related to editing user information            
    def edit_user(event):
        global off_win,txt_btn1,e1

        e1=Entry(off_win,font=('arial',12,'bold'),width=20)
        e1.grid(row=0,column=1,padx=5)
        
        txt_btn1=Label(off_win,font=('arial',12,'bold'),text='Edit Username',padx=2,pady=2,bg="#282424",fg="white")
        txt_btn1.bind("<Button-1>",user)
        txt_btn1.grid(row=0,column=2,sticky=W)

    def pasw(event):
            global e2,txt_btn2,pasw,local_label_2,local_file_dir,off_win

            def work():
                file=open(local_file_dir,'r')
                cred=file.read()
                cred=cred.split('#')
                file.close()

                data=str(cred[0])+'#'+str(pasw)
                
                file=open(local_file_dir,'w')
                file.write(data)
                file.close()
                
            pasw=e2.get()
            e2.destroy()
            txt_btn2.destroy()

            if pasw=="":
                local_label_2.configure(text="Empty")
                work()
            elif pasw.isspace():tk.messagebox.showerror('Error',"A MySQL password that contains only spaces is not permitted. Please provide a password that includes at least one non-space character.")
            else:
                local_label_2.configure(text=pasw)
                work()
    def edit_pasw(event):
        global off_win,txt_btn2,e2

        e2=Entry(off_win,font=('arial',12,'bold'),width=20)
        e2.grid(row=1,column=1,padx=5)
        
        txt_btn2=Label(off_win,font=('arial',12,'bold'),text='Edit Password',padx=2,pady=2,bg="#282424",fg="white")
        txt_btn2.bind("<Button-1>",pasw)
        txt_btn2.grid(row=1,column=2,sticky=W)    
    
    def off():
        global off_win,user,pasw,local_label_1,local_label_2,local_file_dir
        
        off_win=CTk.CTk();off_win.geometry("600x300+350+200");off_win.title("Localhost Credentials");off_win.resizable(0,0)

        current_dir=os.path.dirname(os.path.abspath(__file__))
        local_file_dir=current_dir.replace('Code','')+'TextFiles\\Cache.txt'
        file=open(local_file_dir,'r')
        cred=file.read()
        cred=cred.split('#')
        file.close()

        user,pasw=cred[0],cred[1]

        label=Label(off_win,font=('arial',12,'bold'),text="Your Current Username :   ",padx=2,pady=2,bg="#282424",fg="white").grid(row=0,column=0,sticky=W)
        label=Label(off_win,font=('arial',12,'bold'),text="Your Current Password :   ",padx=2,pady=2,bg="#282424",fg="white").grid(row=1,column=0,sticky=W)

        if user=="":u='Empty'
        else:u=user
        if pasw=="":p='Empty'
        else:p=pasw
        
        local_label_1=Label(off_win,font=('arial',12,'bold'),text=u,padx=2,pady=2,bg="#282424",fg="white")
        local_label_1.bind("<Button-1>",edit_user)
        local_label_1.grid(row=0,column=1,sticky=W)

        local_label_2=Label(off_win,font=('arial',12,'bold'),text=p,padx=2,pady=2,bg="#282424",fg="white")
        local_label_2.bind("<Button-1>",edit_pasw)
        local_label_2.grid(row=1,column=1,sticky=W)

        btn=CTk.CTkButton(off_win,font=('arial',20,'bold'),text="Continue",command=connection)
        btn.place(x=240,y=150)

        btn2=CTk.CTkButton(off_win,text='Back',command=back).place(x=450,y=265)
        
        off_win.mainloop()
# The 'connection()' function attempts to establish a connection to a local MySQL database.
# It uses the 'user' and 'pasw' variables for database authentication.        
    def connection():
        global cur,con,n,user,pasw,off_win
        try:
            n=2
            con=mc.connect(host='localhost',
                           user=str(user),
                           password=str(pasw))
            cur=con.cursor()
            cur.execute("create database if not exists hotelmanagement")
            cur.execute("use hotelmanagement")
            cur.execute("create table if not exists passwords(username varchar(200),password varchar(100))")
            try:
                cur.execute("""create table default_table (Cust_Ref_No int primary key auto_increment,Name varchar(200),Mobile bigint(20),Type_Of_ID varchar(100),ID_No varchar(16),Check_In_Date date,Check_Out_Date date,Room_Type varchar(100),Room_No int,No_Of_Days int,Total_Rent int)auto_increment=1""")
                cur.execute("""INSERT INTO default_table VALUES
(1, 'Amit Kumar', 9876543210, 'Aadhaar Card', '123456789012', '2023-12-15', '2023-12-18', 'Deluxe Room King Bed City View with Bathtub', 129, 3, 25500),
(2, 'Rajat Arora', 9234510976, 'Aadhaar Card', '123456789012', '2023-10-10', '2023-10-19', 'Superior Room with Bathtub, City Views & Twin Bed', 105, 9, 67500),
(3, 'Shlok Kumar', 9212512879, 'Aadhaar Card', '123456789012', '2023-12-20', '2023-12-24', 'Premium Room with Bathtub, Twin Bed & City View', 134, 4, 38000)
""")
            except:pass
            cur.execute("set autocommit=OFF")
            off_win.destroy()
            tk.messagebox.showinfo("Connection Switched","You are switched to the offline mode and you are currently connected the Localhost connection")
            ask()
        except:
            tk.messagebox.showerror("Something went wrong","""An error occurred while attempting to connect to localhost. Please follow these steps to troubleshoot the issue:
1.Ensure that you have MySQL Database Server, MySQL Client, and related components installed and properly configured. You can download and configure them from the official MySQL website.
2.Double-check the provided password and other credentials for accuracy, then try the connection again.
3.If the issue persists, feel free to contact our support team. Our dedicated team will do their best to assist you and resolve the problem.""")
    off()
# The following code defines dictionaries and lists related to room types, room numbers, and tooltips for a hotel management application.
# It includes information about room types, their corresponding rates, available room numbers for each type, and tooltips for user guidance.
# These structures are essential for managing room details and providing helpful information to the user via tooltips.
rooms_dict={'Superior Room with Bathtub, City Views & Twin Bed':7500,
           'Superior Room with Bathtub, City View & King Bed':7500,
            'Deluxe Room Twin Bed City View with Bathtub':8500,
           'Deluxe Room King Bed City View with Bathtub':8500,
            'Premium Room with Bathtub, Twin Bed & City View':9500,
           'Premium Room with Bathtub, City View & King Bed':9500,
            'Premium Room Airport View Twin Bed':10500,
           'Premium Room Airport View King Bed':10500,
            'Deluxe Suite King Bed City View':20000}
room_type_list=[' ','Superior Room with Bathtub, City Views & Twin Bed','Superior Room with Bathtub, City View & King Bed',
                  'Deluxe Room Twin Bed City View with Bathtub','Deluxe Room King Bed City View with Bathtub',
                  'Premium Room with Bathtub, Twin Bed & City View','Premium Room with Bathtub, City View & King Bed',
                  'Premium Room Airport View Twin Bed','Premium Room Airport View King Bed']
room_no_dict={'Superior Room with Bathtub, City Views & Twin Bed':['101','102','103','104','105','106','107','108','109','110'],
                         'Superior Room with Bathtub, City View & King Bed':['110','112','113','114','115','116', '117', '118', '119', '120'],
                         'Deluxe Room Twin Bed City View with Bathtub':['121', '122', '123', '124', '125'],
                         'Deluxe Room King Bed City View with Bathtub':['126', '127', '128', '129', '130'],
                         'Premium Room with Bathtub, Twin Bed & City View':['131', '132', '133', '134', '135'],
                         'Premium Room with Bathtub, City View & King Bed':['136', '137', '138', '139', '140'],
                         'Premium Room Airport View Twin Bed':['141', '142', '143', '144', '145'],'Premium Room Airport View King Bed':['146', '147', '148', '149', '150']}
tooltip_dict={
    'Name':'The Name field should contain only alphabets and spaces, with a minimum of 2 letters.    ',
    'Mobile':'The "Mobile No." field should only contain digits, and the number of digits must be exactly 10.     ',
    'ID_Type':'Please select one of the provided ID Types..     ',
    'Aadhar':"""Aadhaar Card-
Aadhaar Number is a 12 digit individual identification number.""",
"Driving":"""Driving License-
The driving license format consists of 16 characters where-
1)The first two characters are alphabets (letters).
2)Then The third character is a hyphen ('-').
3)And at last The remaining 13 characters are digits (numbers).""",
"Passport":"""Passport-
The format for a valid Indian passport number is:
1)Length: 8 characters.
2)First character: Uppercase alphabet.
3)Next two characters: The first must be a number from 1 to 9, and the second can be any number from 0 to 9.
4)Remaining four characters: Any combination of digits (numbers from 0 to 9).     """,
    'Check-in-Date':'You need to fill the date(in format: YYYY-MM-DD) when you want to check-in into the hotel.     ',
    'Check-out-Date':"""You need to fill the date(in format: YYYY-MM-DD) when you want to check-out into the hotel.
*Note*- The Check-out-Date must fall after the Check-in-Date.     """,
    'Room_Type':'You need to fill in the type of room you want to stay in.     ',
    'Room_No':'You need to fill in the room no. in which you want to stay in.     '
    }
# The conditional block executes the 'intro()' function when the script is run directly.
# This ensures that the introductory information or actions are presented to the user when the program starts.

if __name__=="__main__":
    intro()                      
