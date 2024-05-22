#1 Import statement
import customtkinter
import sqlite3
import bcrypt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image

#2 Initialize main app window
app = customtkinter.CTk()
app.title('Real Estate Management')
app.geometry('850x700')
app.config(bg='#11FFB7')
app.resizable(FALSE, FALSE)

#3 Define fonts
font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold', 'underline')
font5 = ('Arial', 10, 'bold')

#4 Connect to SQLite database
conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()

#5 Create necessary tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS properties(property_id INTEGER PRIMARY KEY, address TEXT, owner TEXT, date_of_purchase TEXT)''')

# Load and prepare the image
logo_image = Image.open("C:/Users/User/Downloads/realestate.png.png")
logo_ctk_image = customtkinter.CTkImage(logo_image, size=(800, 350))

#6 Define functions
def add_property():
    address = address_entry.get()
    owner = owner_entry.get()
    date_of_purchase = date_entry.get()
    
    if address and owner and date_of_purchase:
        cursor.execute('INSERT INTO properties (address, owner, date_of_purchase) VALUES (?, ?, ?)', 
                       (address, owner, date_of_purchase))
        conn.commit()
        messagebox.showinfo('Success', 'Property added successfully.')
        address_entry.delete(0, END)
        owner_entry.delete(0, END)
        date_entry.delete(0, END)
        add_to_treeview()
    else:
        messagebox.showerror('Error', 'Enter all data!')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        cursor.execute('SELECT username FROM users WHERE username=?', (username,))
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            messagebox.showinfo('Success', 'Account has been created.')
            show_login()
    else:
        messagebox.showerror('Error', 'Enter all data!')

def login_account():
    username = username_entry2.get()
    password = password_entry2.get()
    if username and password:
        cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'Logged in successfully')
                property_page()
            else:
                messagebox.showerror('Error', 'Invalid password')
        else:
            messagebox.showerror('Error', 'Invalid Username')
    else:
        messagebox.showerror('Error', 'Enter all data!')

def show_signup():
    frame1.destroy()
    show_signup_frame()

def show_login():
    frame2.destroy()
    show_login_frame()

def property_page():
    frame1.destroy()
    property_frame()

def perm_out():
    frame3.destroy()
    show_login_frame()

def logout():
    response = messagebox.askyesno("Confirm Log out", "Are you sure you want to log out?")
    if response is NO:
        return
    elif response:
        perm_out()

def add_to_treeview():
    cursor.execute('SELECT * FROM properties')
    properties = cursor.fetchall()
    tree.delete(*tree.get_children())
    for property in properties:
        tree.insert('', END, values=property)

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('ERROR', 'Choose a property to delete.')
    else:
        property_id = tree.item(selected_item)['values'][0]  # Assuming 'property_id' is in the first column
        try:
            cursor.execute('DELETE FROM properties WHERE property_id = ?', (property_id,))
            conn.commit()
            add_to_treeview()  # Refresh the Treeview
            messagebox.showinfo('Success', 'Property has been deleted')
        except Exception as e:
            messagebox.showerror('ERROR', f'Failed to delete property: {e}')

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Select a property to update')
    else:
        # Get the current values from the input fields
        address = address_entry.get()
        owner = owner_entry.get()
        date_of_purchase = date_entry.get()

        if not (address and owner and date_of_purchase):
            messagebox.showerror('Error', 'Enter all data!')
            return

        # Get the original property ID from the selected item
        original_property_id = tree.item(selected_item)['values'][0]

        # Update the database
        cursor.execute('''
            UPDATE properties
            SET address = ?, owner = ?, date_of_purchase = ?
            WHERE property_id = ?
        ''', (address, owner, date_of_purchase, original_property_id))
        
        conn.commit()

        # Update the treeview with new data
        add_to_treeview()
        messagebox.showinfo('Success', 'Property has been updated')

        # Clear the entry fields
        address_entry.delete(0, END)
        owner_entry.delete(0, END)
        date_entry.delete(0, END)

# Property Frame
def property_frame():
    global frame3, address_entry, owner_entry, date_entry, tree

    frame3 = customtkinter.CTkFrame(app, bg_color='#7FFFD4', fg_color='#FFFFFF', width=900, height=700)
    frame3.pack(fill='both', expand=True)

    # Top frame for property information input
    frameT = customtkinter.CTkFrame(frame3, bg_color='#7FFFD4', fg_color='#FFFFFF', width=900, height=200)
    frameT.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

    # Address
    address_label = customtkinter.CTkLabel(frameT, font=font2, text='Address:', text_color='#4B0076', bg_color='#FFFFFF')
    address_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    address_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Address',
                                           border_color='#4B0076', border_width=2, width=200)
    address_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Owner Name
    owner_label = customtkinter.CTkLabel(frameT, font=font2, text='Owner Name:', text_color='#4B0076', bg_color='#FFFFFF')
    owner_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')

    owner_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Owner Name',
                                         border_color='#4B0076', border_width=2, width=200)
    owner_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

    # Date of Purchase
    date_label = customtkinter.CTkLabel(frameT, font=font2, text='Date of Purchase:', text_color='#4B0076', bg_color='#FFFFFF')
    date_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    date_entry = customtkinter.CTkEntry(frameT, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Date (YYYY-MM-DD)',
                                        border_color='#4B0076', border_width=2, width=200)
    date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Insert button
    insert_button = customtkinter.CTkButton(frameT, command=add_property, font=font2, text_color='#fff', text='Insert Property',
                                            fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                            corner_radius=5, width=165)
    insert_button.grid(row=1, column=3, padx=10, pady=10, sticky='w')

    # Middle frame for Treeview
    frameM = customtkinter.CTkFrame(frame3, bg_color='#7FFFD4', fg_color='#FFFFFF', width=900, height=400)
    frameM.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

    # Treeview setup
    style = ttk.Style(frameM)
    style.theme_use('clam')
    style.configure('Treeview', font=font3, foreground='#000000', background='#7FFFD4', fieldbackground='#7FFFD4')
    style.configure('Treeview.Heading', font=font3)

    # Treeview
    tree = ttk.Treeview(frameM, columns=('property_id', 'address', 'owner', 'date_of_purchase'), show='headings')
    tree.heading('property_id', text='ID')
    tree.heading('address', text='Address')
    tree.heading('owner', text='Owner')
    tree.heading('date_of_purchase', text='Date of Purchase')
    tree.pack(fill='both', expand=True)

    # Bottom frame for actions
    frameB = customtkinter.CTkFrame(frame3, bg_color='#7FFFD4', fg_color='#FFFFFF', width=900, height=100)
    frameB.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)

    # Update Button
    update_button = customtkinter.CTkButton(frameB, command=update, font=font2, text_color='#fff', text='Update Property',
                                            fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                            corner_radius=5, width=165)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    # Delete Button
    delete_button = customtkinter.CTkButton(frameB, command=delete, font=font2, text_color='#fff', text='Delete Property',
                                            fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                            corner_radius=5, width=165)
    delete_button.grid(row=0, column=1, padx=10, pady=10)

    # Logout Button
    logout_button = customtkinter.CTkButton(frameB, command=logout, font=font2, text_color='#fff', text='Logout',
                                            fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                            corner_radius=5, width=165)
    logout_button.grid(row=0, column=2, padx=10, pady=10)

    # Load properties into the Treeview
    add_to_treeview()

# Login Frame
def show_login_frame():
    global frame1, username_entry2, password_entry2

    frame1 = customtkinter.CTkFrame(app, bg_color='#87CEFA', fg_color='#87CEFA', width=800, height=700)
    frame1.pack(fill='both', expand=True)

    # Logo Frame
    logo_frame = customtkinter.CTkFrame(frame1, width=800, height=350, bg_color='#87CEFA', fg_color='#87CEFA')
    logo_frame.grid(row=0, column=0, padx=20, pady=20)

    # Display logo image
    logo_label = customtkinter.CTkLabel(logo_frame, image=logo_ctk_image, text="")
    logo_label.pack(expand=True)

    # Login Form Frame
    form_frame = customtkinter.CTkFrame(frame1, width=800, height=350, bg_color='#87CEFA', fg_color='#FFF5EE')
    form_frame.grid(row=1, column=0, padx=20, pady=20)

    # Username
    username_label = customtkinter.CTkLabel(form_frame, font=font2, text='Username:', text_color='#4B0076', bg_color='#FFF5EE')
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    username_entry2 = customtkinter.CTkEntry(form_frame, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Username',
                                             border_color='#4B0076', border_width=2, width=200)
    username_entry2.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Password
    password_label = customtkinter.CTkLabel(form_frame, font=font2, text='Password:', text_color='#4B0076', bg_color='#FFF5EE')
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    password_entry2 = customtkinter.CTkEntry(form_frame, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Password',
                                             border_color='#4B0076', border_width=2, width=200, show='*')
    password_entry2.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Login button
    login_button = customtkinter.CTkButton(form_frame, command=login_account, font=font2, text_color='#fff', text='Login',
                                           fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                           corner_radius=5, width=165)
    login_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Signup link
    signup_link = customtkinter.CTkLabel(form_frame, font=font4, text='Don\'t have an account? Signup here',
                                         text_color='#4B0076', bg_color='#FFF5EE', cursor='hand2')
    signup_link.grid(row=3, column=1, padx=10, pady=10, sticky='w')
    signup_link.bind("<Button-1>", lambda e: show_signup())

    # Text label below the login frame
    created_by_label = customtkinter.CTkLabel(frame1, font=font5, text='Created by Kim Carlo and Kyle Andrei', text_color='#4B0076', bg_color='#87CEFA')
    created_by_label.grid(row=2, column=0, pady=10)

# Signup Frame
def show_signup_frame():
    global frame2, username_entry, password_entry

    frame2 = customtkinter.CTkFrame(app, bg_color='#95C8DA', fg_color='#95C8DA', width=800, height=700)
    frame2.pack(fill='both', expand=True)

    # Logo Frame
    logo_frame = customtkinter.CTkFrame(frame2, width=800, height=350, bg_color='#95C8DA', fg_color='#95C8DA')
    logo_frame.grid(row=0, column=0, padx=20, pady=20)

    # Display logo image
    logo_label = customtkinter.CTkLabel(logo_frame, image=logo_ctk_image, text="")
    logo_label.pack(expand=True)

    # Signup Form Frame
    form_frame = customtkinter.CTkFrame(frame2, width=800, height=350, bg_color='#95C8DA', fg_color='#E3E370')
    form_frame.grid(row=1, column=0, padx=20, pady=20)

    # Username
    username_label = customtkinter.CTkLabel(form_frame, font=font2, text='Username:', text_color='#4B0076', bg_color='#E3E370')
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    username_entry = customtkinter.CTkEntry(form_frame, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Username',
                                            border_color='#4B0076', border_width=2, width=200)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Password
    password_label = customtkinter.CTkLabel(form_frame, font=font2, text='Password:', text_color='#4B0076', bg_color='#E3E370')
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    password_entry = customtkinter.CTkEntry(form_frame, font=font2, text_color='#33113D', fg_color='#fff', placeholder_text='Password',
                                            border_color='#4B0076', border_width=2, width=200, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Signup button
    signup_button = customtkinter.CTkButton(form_frame, command=signup, font=font2, text_color='#fff', text='Signup',
                                            fg_color='#4B0076', hover_color='#3C005E', bg_color='#fff', cursor='hand2',
                                            corner_radius=5, width=165)
    signup_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Login link
    login_link = customtkinter.CTkLabel(form_frame, font=font4, text='Already have an account? Login here',
                                        text_color='#4B0076', bg_color='#E3E370', cursor='hand2')
    login_link.grid(row=3, column=1, padx=10, pady=10, sticky='w')
    login_link.bind("<Button-1>", lambda e: show_login())

    # Text label below the login frame
    created_by_label = customtkinter.CTkLabel(frame2, font=font5, text='Created by Kim Carlo and Kyle Andrei', text_color='#4B0076', bg_color='#95C8DA')
    created_by_label.grid(row=2, column=0, pady=10)

# Start with the login frame
show_login_frame()

# Start the app
app.mainloop()
