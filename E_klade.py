﻿import tkinter as tk 
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import bcrypt

# Definējam vienotu loga izmēru
WINDOW_SIZE = "650x400"

########################################
# Datubāzes funkcijas
########################################

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_db_connection():
    conn = sqlite3.connect("app.db")
    conn.execute("PRAGMA encoding = 'UTF-8'")
    return conn

def init_databases():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Lietotāju tabula ar admin statusu
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if c.fetchone() is None:
        c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                  ("admin", hash_password("admin123"), 1))

    # Stundu laiku tabula
    c.execute('''
        CREATE TABLE IF NOT EXISTS stundu_laiki (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stunda TEXT,
            ilgums TEXT,
            starpbridis TEXT
        )
    ''')

    # Ja tabula ir tukša, ievieto sākotnējos datus
    c.execute("SELECT COUNT(*) FROM stundu_laiki")
    count = c.fetchone()[0]
    if count == 0:
        sample_data = [
            ("1.st", "8:15-8:55", "5'"),
            ("2.st", "9:00-9:40", "10'"),
            ("3.st", "9:50-10:30", "10'"),
            ("4.st", "10:40-11:20", "10'"),
            ("5.st", "11:30-12:10", "10'"),
            ("6.st", "12:20-13:00", "10'"),
            ("7.st", "13:10-13:50", "10'"),
            ("8.st", "14:00-14:40", "10'"),
            ("9.st", "14:50-15:30", "5'"),
            ("10.st", "15:35-16:15", " ")
        ]
        c.executemany("INSERT INTO stundu_laiki (stunda, ilgums, starpbridis) VALUES (?,?,?)", sample_data)

    # Stundu saraksta tabula
    c.execute('''
        CREATE TABLE IF NOT EXISTS stundu_saraksts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nedelas_diena TEXT,
            stundas_nr TEXT,
            priekšmets TEXT,
            klase_auditorija TEXT
        )
    ''')

    # Ja tabula ir tukša, ievieto sākotnējos datus
    c.execute("SELECT COUNT(*) FROM stundu_saraksts")
    count = c.fetchone()[0]
    if count == 0:
        sample_data = [
            ("Pirmdiena", "1", "Programmēšana/Ģeogrāfija", "211/210"),
            ("Pirmdiena", "2", "Programmēšana/Ģeogrāfija", "211/210"),
            ("Pirmdiena", "3", "Programmēšana/Ģeogrāfija", "211/210"),
            ("Pirmdiena", "4", "Matemātika", "306"),
            ("Pirmdiena", "5", "2. svešvaloda", "12/19/11"),
            ("Pirmdiena", "6", "2. svešvaloda", "12/19/11"),
            ("Pirmdiena", "7", "Pusdienu brīvstunda", "-"),
            ("Pirmdiena", "8", "-", "-"),
            ("Pirmdiena", "9", "-", "-"),
            ("Otrdiena", "1", "Programmēšana/Ģeogrāfija", "206/210"),
            ("Otrdiena", "2", "Programmēšana/Ģeogrāfija", "206/210"),
            ("Otrdiena", "3", "Programmēšana/Ģeogrāfija", "206/210"),
            ("Otrdiena", "4", "Matemātika ekonomistiem", "208"),
            ("Otrdiena", "5", "Pusdienu brīvstunda", "-"),
            ("Otrdiena", "6", "Sociālās zinātnes", "3"),
            ("Otrdiena", "7", "Sociālās zinātnes", "3"),
            ("Otrdiena", "8", "Matemātika ekonomistiem", "208"),
            ("Otrdiena", "9", "Klases stunda", "306"),
            ("Trešdiena", "1", "Biznesa angļu valoda", "19"),
            ("Trešdiena", "2", "Sociālās zinātnes II", "18"),
            ("Trešdiena", "3", "Sociālās zinātnes II", "18"),
            ("Trešdiena", "4", "1. svešvaloda", "14/6/19"),
            ("Trešdiena", "5", "Matemātika", "306"),
            ("Trešdiena", "6", "Matemātika", "306"),
            ("Trešdiena", "7", "Pusdienu brīvstunda", "-"),
            ("Trešdiena", "8", "Robotika/Uzņēmējdarbība", "201/311"),
            ("Trešdiena", "9", "Robotika/Fakultātes DSD", "201"),
            ("Ceturtdiena", "1", "Literatūra", "10"),
            ("Ceturtdiena", "2", "Literatūra", "10"),
            ("Ceturtdiena", "3", "Sports", "sporta zāle"),
            ("Ceturtdiena", "4", "Sports", "sporta zāle"),
            ("Ceturtdiena", "5", "Pusdienu brīvstunda", "-"),
            ("Ceturtdiena", "6", "1. svešvaloda", "14/13/19"),
            ("Ceturtdiena", "7", "1. svešvaloda", "14/13/19"),
            ("Ceturtdiena", "8", "Robotika/Uzņēmējdarbība", "201/207"),
            ("Ceturtdiena", "9", "Robotika/Uzņēmējdarbība", "201/207"),
            ("Piektdiena", "1", "Latviešu valoda", "10"),
            ("Piektdiena", "2", "Latviešu valoda", "10"),
            ("Piektdiena", "3", "Sociālās zinātnes", "207"),
            ("Piektdiena", "4", "Sociālās zinātnes", "207"),
            ("Piektdiena", "5", "Matemātika", "15"),
            ("Piektdiena", "6", "Matemātika", "15"),
            ("Piektdiena", "7", "Pusdienas/Uzņēmējdarbība", "207"),
            ("Piektdiena", "8", "Pusdienu brīvstunda", "-")
        ]
        c.executemany("INSERT INTO stundu_saraksts (nedelas_diena, stundas_nr, priekšmets, klase_auditorija) VALUES (?,?,?,?)", sample_data)

    conn.commit()
    conn.close()

init_databases()

########################################
# Admin panelis
########################################

class AdminDashboard:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Admin Panelis")
        master.geometry(WINDOW_SIZE)

        tk.Label(master, text="Admin Panelis", font=("Arial", 14)).pack(pady=10)
        tk.Button(master, text="Rediģēt lietotājus", command=self.manage_users).pack(pady=5)
        tk.Button(master, text="Rediģēt stundu laikus", command=self.manage_stundu_laiki).pack(pady=5)
        tk.Button(master, text="Rediģēt stundu sarakstu", command=self.manage_stundu_saraksts).pack(pady=5)
        tk.Button(master, text="Mainīt paroli", command=self.change_password).pack(pady=5)
        tk.Button(master, text="Izrakstīties", command=self.logout).pack(pady=20)

    def change_password(self):
        change_window = tk.Toplevel(self.master)
        change_window.title("Mainīt paroli")
        change_window.geometry("300x200")
        
        tk.Label(change_window, text="Pašreizējā parole:").pack(pady=(10,0))
        current_password_entry = tk.Entry(change_window, show="*")
        current_password_entry.pack()
        
        tk.Label(change_window, text="Jaunā parole:").pack(pady=(10,0))
        new_password_entry = tk.Entry(change_window, show="*")
        new_password_entry.pack()
        
        tk.Label(change_window, text="Atkārto jauno paroli:").pack(pady=(10,0))
        repeat_password_entry = tk.Entry(change_window, show="*")
        repeat_password_entry.pack()
        
        def save_new_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            repeat_password = repeat_password_entry.get()
            
            if not current_password or not new_password or not repeat_password:
                messagebox.showerror("Kļūda", "Visi lauki ir obligāti!")
                return
                
            if new_password != repeat_password:
                messagebox.showerror("Kļūda", "Jaunās paroles nesakrīt!")
                return
                
            if len(new_password) < 6:
                messagebox.showerror("Kļūda", "Parolei jābūt vismaz 6 simbolu garai!")
                return
                
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (self.username,))
            result = c.fetchone()
            
            if result and check_password(current_password, result[0]):
                c.execute("UPDATE users SET password=? WHERE username=?", 
                          (hash_password(new_password), self.username))
                conn.commit()
                messagebox.showinfo("Panākumi", "Parole veiksmīgi nomainīta!")
                change_window.destroy()
            else:
                messagebox.showerror("Kļūda", "Nepareiza pašreizējā parole!")
            conn.close()
        
        tk.Button(change_window, text="Saglabāt", command=save_new_password).pack(pady=10)

    def manage_users(self):
        user_window = tk.Toplevel(self.master)
        user_window.title("Rediģēt lietotājus")
        user_window.geometry(WINDOW_SIZE)

        tree = ttk.Treeview(user_window, columns=("ID", "Lietotājvārds", "Admin statuss"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Lietotājvārds", text="Lietotājvārds")
        tree.heading("Admin statuss", text="Admin statuss")
        tree.column("ID", width=30)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, username, is_admin FROM users")
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        load_data()

        def add_user():
            add_window = tk.Toplevel(user_window)
            add_window.title("Pievienot jaunu lietotāju")
            add_window.geometry("300x200")
            
            tk.Label(add_window, text="Lietotājvārds:").pack(pady=(10,0))
            username_entry = tk.Entry(add_window)
            username_entry.pack()
            
            tk.Label(add_window, text="Parole:").pack(pady=(10,0))
            password_entry = tk.Entry(add_window, show="*")
            password_entry.pack()
            
            admin_var = tk.IntVar()
            tk.Checkbutton(add_window, text="Administrators", variable=admin_var).pack(pady=(10,0))
            
            def save_user():
                username = username_entry.get()
                password = password_entry.get()
                is_admin = admin_var.get()
                
                if not username or not password:
                    messagebox.showerror("Kļūda", "Lietotājvārds un parole nevar būt tukši!")
                    return
                    
                if len(password) < 6:
                    messagebox.showerror("Kļūda", "Parolei jābūt vismaz 6 simbolu garai!")
                    return
                    
                conn = get_db_connection()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                              (username, hash_password(password), is_admin))
                    conn.commit()
                    messagebox.showinfo("Panākumi", "Lietotājs veiksmīgi pievienots!")
                    load_data()
                    add_window.destroy()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Kļūda", "Lietotājvārds jau eksistē!")
                finally:
                    conn.close()
            
            btn_frame = tk.Frame(add_window)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Saglabāt", command=save_user).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Atcelt", command=add_window.destroy).pack(side=tk.LEFT, padx=5)

        def edit_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru rediģēt.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            new_username = simpledialog.askstring("Rediģēt", "Ievadiet jauno lietotājvārdu:", initialvalue=record[1])
            if new_username is None:
                return
            new_admin = simpledialog.askinteger("Rediģēt", "Vai lietotājs ir administrators? (0 – nav, 1 – ir):", initialvalue=record[2])
            if new_admin is None or new_admin not in (0, 1):
                messagebox.showerror("Kļūda", "Lūdzu ievadiet derīgu vērtību (0 vai 1)!")
                return
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE users SET username=?, is_admin=? WHERE id=?", (new_username, new_admin, record_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Panākumi", "Lietotājs atjaunināts!")
            load_data()

        def delete_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru dzēst.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            confirm = messagebox.askyesno("Apstiprinājums", "Vai tiešām vēlaties dzēst šo lietotāju?")
            if confirm:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("DELETE FROM users WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Panākumi", "Lietotājs dzēsts!")
                load_data()

        btn_frame = tk.Frame(user_window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Pievienot jaunu", command=add_user).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Rediģēt izvēlēto", command=edit_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Dzēst izvēlēto", command=delete_record).pack(side=tk.LEFT, padx=5)

    def manage_stundu_laiki(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Rediģēt stundu laikus")
        edit_window.geometry(WINDOW_SIZE)

        tree = ttk.Treeview(edit_window, columns=("ID", "Stunda", "Ilgums", "Starpbridis"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Stunda", text="Stunda")
        tree.heading("Ilgums", text="Ilgums")
        tree.heading("Starpbridis", text="Starpbridis")
        tree.column("ID", width=30)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, stunda, ilgums, starpbridis FROM stundu_laiki")
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        load_data()

        def edit_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru rediģēt.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            new_stunda = simpledialog.askstring("Rediģēt", "Ievadiet jauno stundu:", initialvalue=record[1])
            if new_stunda is None:
                return
            new_ilgums = simpledialog.askstring("Rediģēt", "Ievadiet jaunu ilgumu:", initialvalue=record[2])
            if new_ilgums is None:
                return
            new_starpbridis = simpledialog.askstring("Rediģēt", "Ievadiet jaunu starpbrīdi:", initialvalue=record[3])
            if new_starpbridis is None:
                return
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE stundu_laiki SET stunda=?, ilgums=?, starpbridis=? WHERE id=?",
                      (new_stunda, new_ilgums, new_starpbridis, record_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Panākumi", "Ieraksts atjaunināts!")
            load_data()

        def delete_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru dzēst.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            confirm = messagebox.askyesno("Apstiprinājums", "Vai tiešām vēlaties dzēst šo ierakstu?")
            if confirm:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("DELETE FROM stundu_laiki WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Panākumi", "Ieraksts dzēsts!")
                load_data()

        btn_frame = tk.Frame(edit_window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Rediģēt izvēlēto", command=edit_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Dzēst izvēlēto", command=delete_record).pack(side=tk.LEFT, padx=5)

    def manage_stundu_saraksts(self):
        saraksts_window = tk.Toplevel(self.master)
        saraksts_window.title("Rediģēt stundu sarakstu")
        saraksts_window.geometry(WINDOW_SIZE)

        tree = ttk.Treeview(saraksts_window, columns=("ID", "Diena", "Stunda", "Priekšmets", "Klase/Auditorija"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Diena", text="Nedēļas diena")
        tree.heading("Stunda", text="Stundas nr.")
        tree.heading("Priekšmets", text="Priekšmets")
        tree.heading("Klase/Auditorija", text="Klase/Auditorija")
        tree.column("ID", width=30)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id, nedelas_diena, stundas_nr, priekšmets, klase_auditorija FROM stundu_saraksts ORDER BY "
                      "CASE nedelas_diena "
                      "WHEN 'Pirmdiena' THEN 1 "
                      "WHEN 'Otrdiena' THEN 2 "
                      "WHEN 'Trešdiena' THEN 3 "
                      "WHEN 'Ceturtdiena' THEN 4 "
                      "WHEN 'Piektdiena' THEN 5 "
                      "END, stundas_nr")
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        load_data()

        def add_record():
            add_window = tk.Toplevel(saraksts_window)
            add_window.title("Pievienot jaunu stundu")
            add_window.geometry("400x300")
            
            tk.Label(add_window, text="Nedēļas diena:").pack(pady=(10,0))
            diena_var = tk.StringVar()
            diena_combobox = ttk.Combobox(add_window, textvariable=diena_var, 
                                        values=["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturtdiena", "Piektdiena"])
            diena_combobox.pack()
            
            tk.Label(add_window, text="Stundas nr:").pack(pady=(10,0))
            stunda_entry = tk.Entry(add_window)
            stunda_entry.pack()
            
            tk.Label(add_window, text="Priekšmets:").pack(pady=(10,0))
            priekšmets_entry = tk.Entry(add_window)
            priekšmets_entry.pack()
            
            tk.Label(add_window, text="Klase/Auditorija:").pack(pady=(10,0))
            klase_entry = tk.Entry(add_window)
            klase_entry.pack()
            
            def save_record():
                diena = diena_var.get()
                stunda = stunda_entry.get()
                priekšmets = priekšmets_entry.get()
                klase = klase_entry.get()
                
                if not diena or not stunda or not priekšmets or not klase:
                    messagebox.showerror("Kļūda", "Visi lauki ir obligāti!")
                    return
                    
                conn = get_db_connection()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO stundu_saraksts (nedelas_diena, stundas_nr, priekšmets, klase_auditorija) VALUES (?, ?, ?, ?)",
                              (diena, stunda, priekšmets, klase))
                    conn.commit()
                    messagebox.showinfo("Panākumi", "Stunda veiksmīgi pievienota!")
                    load_data()
                    add_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Kļūda", f"Datubāzes kļūda: {e}")
                finally:
                    conn.close()
            
            btn_frame = tk.Frame(add_window)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Saglabāt", command=save_record).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Atcelt", command=add_window.destroy).pack(side=tk.LEFT, padx=5)

        def edit_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru rediģēt.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            
            edit_window = tk.Toplevel(saraksts_window)
            edit_window.title("Rediģēt stundu")
            edit_window.geometry("400x300")
            
            tk.Label(edit_window, text="Nedēļas diena:").pack(pady=(10,0))
            diena_var = tk.StringVar(value=record[1])
            diena_combobox = ttk.Combobox(edit_window, textvariable=diena_var, 
                                        values=["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturtdiena", "Piektdiena"])
            diena_combobox.pack()
            
            tk.Label(edit_window, text="Stundas nr:").pack(pady=(10,0))
            stunda_entry = tk.Entry(edit_window)
            stunda_entry.insert(0, record[2])
            stunda_entry.pack()
            
            tk.Label(edit_window, text="Priekšmets:").pack(pady=(10,0))
            priekšmets_entry = tk.Entry(edit_window)
            priekšmets_entry.insert(0, record[3])
            priekšmets_entry.pack()
            
            tk.Label(edit_window, text="Klase/Auditorija:").pack(pady=(10,0))
            klase_entry = tk.Entry(edit_window)
            klase_entry.insert(0, record[4])
            klase_entry.pack()
            
            def update_record():
                diena = diena_var.get()
                stunda = stunda_entry.get()
                priekšmets = priekšmets_entry.get()
                klase = klase_entry.get()
                
                if not diena or not stunda or not priekšmets or not klase:
                    messagebox.showerror("Kļūda", "Visi lauki ir obligāti!")
                    return
                    
                conn = get_db_connection()
                c = conn.cursor()
                try:
                    c.execute("UPDATE stundu_saraksts SET nedelas_diena=?, stundas_nr=?, priekšmets=?, klase_auditorija=? WHERE id=?",
                              (diena, stunda, priekšmets, klase, record_id))
                    conn.commit()
                    messagebox.showinfo("Panākumi", "Stunda veiksmīgi atjaunināta!")
                    load_data()
                    edit_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Kļūda", f"Datubāzes kļūda: {e}")
                finally:
                    conn.close()
            
            btn_frame = tk.Frame(edit_window)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Saglabāt", command=update_record).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Atcelt", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)

        def delete_record():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Brīdinājums", "Lūdzu izvēlieties ierakstu, kuru dzēst.")
                return
            record = tree.item(selected_item)["values"]
            record_id = record[0]
            confirm = messagebox.askyesno("Apstiprinājums", "Vai tiešām vēlaties dzēst šo stundu?")
            if confirm:
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("DELETE FROM stundu_saraksts WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Panākumi", "Stunda dzēsta!")
                load_data()

        btn_frame = tk.Frame(saraksts_window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Pievienot jaunu", command=add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Rediģēt izvēlēto", command=edit_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Dzēst izvēlēto", command=delete_record).pack(side=tk.LEFT, padx=5)

    def logout(self):
        self.master.destroy()
        main()

########################################
# Lietotāja panelis
########################################

class UserDashboard:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("E-klade")
        master.geometry(WINDOW_SIZE)

        tk.Label(master, text="E-klade", font=("Arial", 14)).pack(pady=10)
        tk.Button(master, text="Apskatīt stundu laikus", command=self.view_stundu_laiki).pack(pady=5)
        tk.Button(master, text="Apskatīt stundu sarakstu", command=self.view_stundu_saraksts).pack(pady=5)
        tk.Button(master, text="Mainīt paroli", command=self.change_password).pack(pady=5)
        tk.Button(master, text="Izrakstīties", command=self.logout).pack(pady=20)

    def change_password(self):
        change_window = tk.Toplevel(self.master)
        change_window.title("Mainīt paroli")
        change_window.geometry("300x200")
        
        tk.Label(change_window, text="Pašreizējā parole:").pack(pady=(10,0))
        current_password_entry = tk.Entry(change_window, show="*")
        current_password_entry.pack()
        
        tk.Label(change_window, text="Jaunā parole:").pack(pady=(10,0))
        new_password_entry = tk.Entry(change_window, show="*")
        new_password_entry.pack()
        
        tk.Label(change_window, text="Atkārto jauno paroli:").pack(pady=(10,0))
        repeat_password_entry = tk.Entry(change_window, show="*")
        repeat_password_entry.pack()
        
        def save_new_password():
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            repeat_password = repeat_password_entry.get()
            
            if not current_password or not new_password or not repeat_password:
                messagebox.showerror("Kļūda", "Visi lauki ir obligāti!")
                return
                
            if new_password != repeat_password:
                messagebox.showerror("Kļūda", "Jaunās paroles nesakrīt!")
                return
                
            if len(new_password) < 6:
                messagebox.showerror("Kļūda", "Parolei jābūt vismaz 6 simbolu garai!")
                return
                
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username=?", (self.username,))
            result = c.fetchone()
            
            if result and check_password(current_password, result[0]):
                c.execute("UPDATE users SET password=? WHERE username=?", 
                          (hash_password(new_password), self.username))
                conn.commit()
                messagebox.showinfo("Panākumi", "Parole veiksmīgi nomainīta!")
                change_window.destroy()
            else:
                messagebox.showerror("Kļūda", "Nepareiza pašreizējā parole!")
            conn.close()
        
        tk.Button(change_window, text="Saglabāt", command=save_new_password).pack(pady=10)

    def view_stundu_laiki(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("Stundu laiki")
        view_window.geometry(WINDOW_SIZE)

        tree = ttk.Treeview(view_window, columns=("Stunda", "Ilgums", "Starpbridis"), show='headings')
        tree.heading("Stunda", text="Stunda")
        tree.heading("Ilgums", text="Ilgums")
        tree.heading("Starpbridis", text="Starpbridis")

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT stunda, ilgums, starpbridis FROM stundu_laiki")
        for row in c.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

        tree.pack(fill=tk.BOTH, expand=True)

    def view_stundu_saraksts(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("Stundu saraksts")
        view_window.geometry(WINDOW_SIZE)

        # Izveidojam Notebook (cilnes) katram dienai
        notebook = ttk.Notebook(view_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        conn = get_db_connection()
        c = conn.cursor()

        dienas = ["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturtdiena", "Piektdiena"]
        
        for diena in dienas:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=diena)
            
            tree = ttk.Treeview(frame, columns=("Stunda", "Priekšmets", "Klase/Auditorija"), show='headings')
            tree.heading("Stunda", text="Stundas nr.")
            tree.heading("Priekšmets", text="Priekšmets")
            tree.heading("Klase/Auditorija", text="Klase/Auditorija")
            
            c.execute("SELECT stundas_nr, priekšmets, klase_auditorija FROM stundu_saraksts WHERE nedelas_diena=? ORDER BY stundas_nr", (diena,))
            for row in c.fetchall():
                tree.insert("", "end", values=row)
                
            tree.pack(fill=tk.BOTH, expand=True)

        conn.close()

    def logout(self):
        self.master.destroy()
        main()

########################################
# Pieslēgšanās un reģistrācijas logs
########################################

class App:
    def __init__(self, master):
        self.master = master
        master.title("Autentifikācija")
        master.geometry(WINDOW_SIZE)

        tk.Label(master, text="Lietotājvārds:").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()
        self.username_entry.focus()

        tk.Label(master, text="Parole:").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Pieslēgties", command=self.login).pack()
        tk.Button(master, text="Reģistrēties", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT username, password, is_admin FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password(password, user[1]):
            self.master.destroy()
            root = tk.Tk()
            if user[2] == 1:
                AdminDashboard(root, username)
            else:
                UserDashboard(root, username)
            root.mainloop()
        else:
            messagebox.showerror("Kļūda", "Nepareizs lietotājvārds vai parole")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if len(password) < 6:
            messagebox.showerror("Kļūda", "Parolei jābūt vismaz 6 simbolu garai!")
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            messagebox.showerror("Kļūda", "Lietotājvārds jau eksistē")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hash_password(password)))
            conn.commit()
            messagebox.showinfo("Reģistrācija", "Lietotājs veiksmīgi reģistrēts")
        conn.close()

########################################
# Palaišanas funkcija
########################################

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
