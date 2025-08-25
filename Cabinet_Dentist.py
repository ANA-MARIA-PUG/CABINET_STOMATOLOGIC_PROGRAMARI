import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import datetime
import csv
import os

# ---------------- CONFIG ------------------
CSV_FILE = "programari.csv"
USERNAME = "ana"
PAROLA = "anamariapug"
programari = []

# ---------------- SMS PLACEHOLDER ------------------
def trimite_sms(telefon, mesaj): 
    print(f"[FAKE SMS] către {telefon}: {mesaj}")

# ---------------- LOGIN ------------------
def login():
    user = entry_user.get().strip()
    parola = entry_pass.get().strip()
    if user == USERNAME and parola == PAROLA:
        login_window.destroy()
        porneste_aplicatia()
    else:
        messagebox.showerror("Eroare", "Autentificare eșuată. Verifică userul sau parola.")

# ---------------- FUNCTIONALITĂȚI ------------------
def adauga_programare():
    nume = entry_nume.get().strip()
    telefon = entry_telefon.get().strip()
    email = entry_email.get().strip()
    data = entry_data.get().strip()
    ora = entry_ora.get().strip()

    if not all([nume, telefon, email, data, ora]):
        messagebox.showwarning("Completare", "Toate câmpurile sunt obligatorii.")
        return

    if not telefon.isdigit() or len(telefon) != 10:
        messagebox.showerror("Telefon greșit", "Numărul de telefon trebuie să aibă exact 10 cifre.")
        return

    try:
        datetime.datetime.strptime(data, "%Y-%m-%d")
        datetime.datetime.strptime(ora, "%H:%M")
    except ValueError:
        messagebox.showerror("Format greșit", "Data trebuie în format YYYY-MM-DD și ora HH:MM.")
        return

    programari.append((nume, telefon, email, data, ora))
    salveaza_csv()
    update_tabel()
    clear_fields()

    mesaj = f"Reminder: Programare la cabinetul stomatologic pe {data} la ora {ora}."
    trimite_sms(telefon, mesaj)
    messagebox.showinfo("Succes", "Programarea a fost adăugată și SMS-ul a fost trimis.")

def sterge_programare_selectata():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selecție", "Selectează o programare pentru ștergere.")
        return

    index = tree.index(selected[0])
    if 0 <= index < len(programari):
        del programari[index]
        salveaza_csv()
        update_tabel()

def update_tabel():
    tree.delete(*tree.get_children())
    for prog in programari:
        tree.insert("", "end", values=prog)

def clear_fields():
    entry_nume.delete(0, "end")
    entry_telefon.delete(0, "end")
    entry_email.delete(0, "end")
    entry_data.delete(0, "end")
    entry_ora.delete(0, "end")

def salveaza_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(programari)

def incarca_csv():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 5:
                    programari.append(tuple(row))

# ---------------- CAUTARE ------------------
def cauta_programari():
    nume_cautat = entry_cautare.get().strip().lower()
    if not nume_cautat:
        update_tabel()
        return

    rezultate = [prog for prog in programari if nume_cautat in prog[0].lower()]
    if not rezultate:
        messagebox.showinfo("Căutare", f"Niciun pacient găsit cu numele '{nume_cautat}'.")
    else:
        tree.delete(*tree.get_children())
        for prog in rezultate:
            tree.insert("", "end", values=prog)

# ---------------- INTERFAȚA PRINCIPALĂ ------------------
def porneste_aplicatia():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    global app, entry_nume, entry_telefon, entry_email, entry_data, entry_ora, tree, entry_cautare

    app = ctk.CTk()
    app.title("🦷 Cabinet Stomatologic - Programări")
    app.geometry("750x650")

    frame_form = ctk.CTkFrame(app)
    frame_form.pack(pady=20, padx=20, fill="x")

    labels = ["Nume", "Telefon (10 cifre)", "Email", "Data (YYYY-MM-DD)", "Ora (HH:MM)"]
    entries = []

    for i, text in enumerate(labels):
        ctk.CTkLabel(frame_form, text=text).grid(row=i, column=0, pady=6, sticky="e")
        entry = ctk.CTkEntry(frame_form, width=300)
        entry.grid(row=i, column=1, pady=6, padx=10)
        entries.append(entry)

    entry_nume, entry_telefon, entry_email, entry_data, entry_ora = entries

    ctk.CTkButton(app, text="➕ Adaugă Programare", command=adauga_programare).pack(pady=10)

    # === CĂUTARE PACIENT ===
    frame_cautare = ctk.CTkFrame(app)
    frame_cautare.pack(pady=5)

    entry_cautare = ctk.CTkEntry(frame_cautare, width=250, placeholder_text="Caută după nume")
    entry_cautare.pack(side="left", padx=10)

    ctk.CTkButton(frame_cautare, text="🔍 Caută", command=cauta_programari).pack(side="left", padx=5)
    ctk.CTkButton(frame_cautare, text="🔄 Reset", command=update_tabel).pack(side="left", padx=5)

    # === TABEL PROGRAMARI ===
    tree = ttk.Treeview(app, columns=("Nume", "Telefon", "Email", "Data", "Ora"), show="headings", height=10)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#1f6aa5", foreground="white")
    style.configure("Treeview", font=("Segoe UI", 10), background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white", rowheight=28)

    for col in ("Nume", "Telefon", "Email", "Data", "Ora"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=130)
    tree.pack(pady=10, padx=20, fill="both", expand=True)

    ctk.CTkButton(app, text="🗑️ Șterge Programare", command=sterge_programare_selectata).pack(pady=5)

    incarca_csv()
    update_tabel()
    app.mainloop()

# ---------------- FEREASTRA LOGIN ------------------
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

login_window = ctk.CTk()
login_window.title("Autentificare")
login_window.geometry("350x250")
login_window.resizable(False, False)

frame_login = ctk.CTkFrame(login_window)
frame_login.pack(pady=30, padx=20)

ctk.CTkLabel(frame_login, text="Username:").grid(row=0, column=0, pady=10, sticky="e")
entry_user = ctk.CTkEntry(frame_login)
entry_user.grid(row=0, column=1, pady=10, padx=5)

ctk.CTkLabel(frame_login, text="Parolă:").grid(row=1, column=0, pady=10, sticky="e")
entry_pass = ctk.CTkEntry(frame_login, show="*")
entry_pass.grid(row=1, column=1, pady=10, padx=5)

ctk.CTkButton(login_window, text="🔐 Login", command=login).pack(pady=10)
login_window.mainloop()
