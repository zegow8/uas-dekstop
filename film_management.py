import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import customtkinter as ctk  

def connect_db():
    """Koneksi ke database SQLite."""
    conn = sqlite3.connect("film_db.sqlite")
    return conn

def init_db():
    """Inisialisasi tabel database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        rating REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_film():
    """Tambah data film baru."""
    title, genre, year, rating = entry_title.get(), entry_genre.get(), entry_year.get(), entry_rating.get()
    if not title or not genre or not year or not rating:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO films (title, genre, year, rating) VALUES (?, ?, ?, ?)", 
                       (title, genre, int(year), float(rating)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Film berhasil ditambahkan!")
        clear_entries()
        fetch_films()
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def edit_film():
    """Edit data film yang dipilih."""
    selected_item = film_table.selection()
    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih data yang mau diedit!")
        return
    try:
        film_id = film_table.item(selected_item[0], "values")[0]
        title, genre, year, rating = entry_title.get(), entry_genre.get(), entry_year.get(), entry_rating.get()
        if not title or not genre or not year or not rating:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE films SET title = ?, genre = ?, year = ?, rating = ? WHERE id = ?", 
                       (title, genre, int(year), float(rating), film_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukses", "Film berhasil diperbarui!")
        clear_entries()
        fetch_films()
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete_film():
    """Hapus data film yang dipilih."""
    selected_item = film_table.selection()
    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih data yang mau dihapus!")
        return
    confirm = messagebox.askyesno("Konfirmasi", "Yakin mau hapus data ini?")
    if confirm:
        try:
            film_id = film_table.item(selected_item[0], "values")[0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM films WHERE id = ?", (film_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Film berhasil dihapus!")
            fetch_films()
        except Exception as e:
            messagebox.showerror("Error", f"Kesalahan: {e}")

def fetch_films(search_term=""):
    """Ambil data semua film dan tampilkan di tabel, dengan opsi pencarian."""
    for item in film_table.get_children():
        film_table.delete(item)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if search_term:
            cursor.execute("SELECT * FROM films WHERE title LIKE ? OR genre LIKE ?", 
                           ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute("SELECT * FROM films")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            film_table.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def search_films():
    """Mencari film berdasarkan judul atau genre."""
    search_term = entry_search.get()
    fetch_films(search_term)

def clear_entries():
    """Bersihkan semua input."""
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)
    entry_search.delete(0, tk.END)

root = ctk.CTk()
root.geometry("800x600")
root.title("Manajemen Film Favorit")

root.configure(bg="#800000")

header_label = ctk.CTkLabel(root, text="APLIKASI DESKTOP MANAJEMEN FILM BIOSKOP", 
                            font=("Ariel", 20, "bold"), text_color="white", 
                            fg_color="#800000", pady=20)
header_label.pack(fill="x", padx=20)

frame_input = ctk.CTkFrame(root)
frame_input.pack(pady=20)

# Input form fields
ctk.CTkLabel(frame_input, text="Judul").grid(row=0, column=0, padx=10, pady=5)
entry_title = ctk.CTkEntry(frame_input)
entry_title.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_input, text="Genre").grid(row=1, column=0, padx=10, pady=5)
entry_genre = ctk.CTkEntry(frame_input)
entry_genre.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_input, text="Tahun").grid(row=2, column=0, padx=10, pady=5)
entry_year = ctk.CTkEntry(frame_input)
entry_year.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_input, text="Rating").grid(row=3, column=0, padx=10, pady=5)
entry_rating = ctk.CTkEntry(frame_input)
entry_rating.grid(row=3, column=1, padx=10, pady=5)

# Search field
ctk.CTkLabel(root, text="Cari Film").pack(pady=10)
entry_search = ctk.CTkEntry(root)
entry_search.pack(pady=10, padx=20)
ctk.CTkButton(root, text="Cari", command=search_films, fg_color="#800000").pack(pady=10)

columns = ("ID", "Judul", "Genre", "Tahun", "Rating")
film_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    film_table.heading(col, text=col)
film_table.pack(pady=20)

frame_buttons = ctk.CTkFrame(root)
frame_buttons.pack(pady=10)

# Buttons
ctk.CTkButton(frame_buttons, text="Tambah Film", command=add_film, fg_color="#800000").grid(row=0, column=0, padx=10, pady=5)
ctk.CTkButton(frame_buttons, text="Edit Film", command=edit_film, fg_color="#800000").grid(row=0, column=1, padx=10, pady=5)
ctk.CTkButton(frame_buttons, text="Hapus Film", command=delete_film, fg_color="#800000").grid(row=0, column=2, padx=10, pady=5)
ctk.CTkButton(frame_buttons, text="Refresh", command=fetch_films, fg_color="#800000").grid(row=0, column=3, padx=10, pady=5)

init_db()
fetch_films()

root.mainloop()
