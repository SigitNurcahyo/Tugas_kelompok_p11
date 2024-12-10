import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="library_oke"
    )

# Fungsi untuk menambahkan data buku baru ke database
def create_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    genre = entry_genre.get()

    # Memastikan semua kolom diisi sebelum menyimpan data
    if title and author and year and genre:
        connection = create_connection()
        cursor = connection.cursor()

        # Query untuk menambahkan data ke tabel books
        query = "INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, author, year, genre))
        connection.commit()  # Menyimpan perubahan ke database

        cursor.close()
        connection.close()

        # Memberikan pesan sukses setelah data disimpan
        messagebox.showinfo("Sukses", f"Buku '{title}' berhasil ditambahkan!")
        clear_fields()  # Membersihkan input setelah data disimpan
        listbox_books.delete(0, tk.END)
        read_books()  # Memperbarui daftar buku
    else:
        # Memberikan peringatan jika ada kolom yang kosong
        messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom.")

# Fungsi untuk membaca data dari tabel books dan menampilkan ke Listbox
def read_books():
    connection = create_connection()
    cursor = connection.cursor()

    # Query untuk mengambil semua data dari tabel books
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    # Membersihkan Listbox sebelum menampilkan data baru
    listbox_books.delete(0, tk.END)
    for row in books:
        listbox_books.insert(tk.END, f"ID: {row[0]} | Judul: {row[1]} | Penulis: {row[2]} | Tahun: {row[3]} | Genre: {row[4]}")

    cursor.close()
    connection.close()

# Fungsi untuk menghapus buku yang dipilih
def delete_book():
    selected_book = listbox_books.curselection()
    if selected_book:
        # Mendapatkan ID buku dari teks yang dipilih di Listbox
        book_info = listbox_books.get(selected_book).split("|")[0]
        book_id = book_info.split(": ")[1].strip()

        connection = create_connection()
        cursor = connection.cursor()

        # Query untuk menghapus buku berdasarkan ID
        query = "DELETE FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        connection.commit()

        cursor.close()
        connection.close()

        # Memberikan pesan sukses dan memperbarui daftar buku
        messagebox.showinfo("Sukses", f"Buku dengan ID {book_id} berhasil dihapus!")
        listbox_books.delete(0, tk.END)
        read_books()
    else:
        # Memberikan peringatan jika tidak ada buku yang dipilih
        messagebox.showwarning("Kesalahan Pilihan", "Pilih data buku yang ingin dihapus.")

# Fungsi untuk mengaktifkan mode edit pada buku yang dipilih
def update_book(event=None):
    selected_book = listbox_books.curselection()
    if selected_book:
        # Mendapatkan ID buku dari teks yang dipilih di Listbox
        book_info = listbox_books.get(selected_book).split("|")[0]
        book_id = book_info.split(": ")[1].strip()

        connection = create_connection()
        cursor = connection.cursor()

        # Query untuk mengambil data buku berdasarkan ID
        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        cursor.close()
        connection.close()

        if book:
            # Menampilkan data buku ke kolom input untuk diedit
            entry_title.delete(0, tk.END)
            entry_title.insert(0, book[1])

            entry_author.delete(0, tk.END)
            entry_author.insert(0, book[2])

            entry_year.delete(0, tk.END)
            entry_year.insert(0, book[3])

            entry_genre.delete(0, tk.END)
            entry_genre.insert(0, book[4])

            # Pesan info bahwa mode edit aktif
            messagebox.showinfo("Edit Mode", "Edit kolom dan klik 'Simpan Perubahan' untuk memperbarui.")
        else:
            messagebox.showwarning("Kesalahan", "Data buku tidak dapat ditemukan.")
    else:
        messagebox.showwarning("Kesalahan Pilihan", "Pilih data buku yang ingin diedit.")

# Fungsi untuk menyimpan perubahan data buku yang sedang diedit
def save_changes():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    genre = entry_genre.get()

    selected_book = listbox_books.curselection()
    if selected_book:
        # Mendapatkan ID buku dari teks yang dipilih di Listbox
        book_info = listbox_books.get(selected_book).split("|")[0]
        book_id = book_info.split(": ")[1].strip()

        # Memastikan semua kolom diisi sebelum menyimpan perubahan
        if title and author and year and genre:
            connection = create_connection()
            cursor = connection.cursor()

            # Query untuk memperbarui data buku berdasarkan ID
            query = """
            UPDATE books 
            SET title = %s, author = %s, year = %s, genre = %s 
            WHERE id = %s
            """
            cursor.execute(query, (title, author, year, genre, book_id))
            connection.commit()

            cursor.close()
            connection.close()

            # Memberikan pesan sukses dan memperbarui daftar buku
            messagebox.showinfo("Sukses", f"Buku dengan ID {book_id} berhasil diperbarui!")
            clear_fields()  # Membersihkan input setelah disimpan
            listbox_books.delete(0, tk.END)
            read_books()
        else:
            messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom.")
    else:
        messagebox.showwarning("Kesalahan Pilihan", "Pilih data buku yang ingin disimpan.")

# Fungsi untuk membersihkan semua kolom input
def clear_fields():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_genre.delete(0, tk.END)

# Fungsi untuk membuat antarmuka pengguna (GUI)
def create_gui():
    global entry_title, entry_author, entry_year, entry_genre, listbox_books

    # Membuat jendela utama
    root = tk.Tk()
    root.title("Manajemen Perpustakaan")
    root.geometry("900x650")
    root.config(bg="#f5f5f5")

    # Membuat header
    header_frame = tk.Frame(root, bg="#003865")
    header_frame.pack(fill=tk.X)
    tk.Label(
        header_frame, text="Sistem Manajemen Perpustakaan", 
        font=("Arial", 18, "bold"), bg="#003865", fg="white", pady=15
    ).pack()

    # Membuat frame untuk input data
    frame_input = tk.Frame(root, bg="#ffffff")
    frame_input.pack(pady=20)

    font_style = ("Arial", 12)
    labels = ["Judul Buku:", "Penulis:", "Tahun Terbit:", "Genre:"]
    entries = []
    for i, label in enumerate(labels):
        # Menambahkan label dan input field
        tk.Label(frame_input, text=label, font=font_style, bg="#ffffff", fg="#003865").grid(row=i, column=0, padx=15, pady=5, sticky="w")
        entry = tk.Entry(frame_input, font=font_style, width=40, bg="#f0f0f0")
        entry.grid(row=i, column=1, padx=15, pady=5)
        entries.append(entry)

    # Menyimpan referensi ke input field
    entry_title, entry_author, entry_year, entry_genre = entries

    # Membuat frame untuk tombol
    frame_buttons = tk.Frame(root, bg="#ffffff")
    frame_buttons.pack(pady=10)

    # Menambahkan tombol dengan fungsinya masing-masing
    button_data = [
        ("Tambah Buku", "#4CAF50", create_book),
        ("Hapus Buku", "#F44336", delete_book),
        ("Edit Buku", "#FFC107", update_book),
        ("Simpan Perubahan", "#2196F3", save_changes),
    ]

    for text, color, command in button_data:
        button = tk.Button(
            frame_buttons, text=text, font=font_style, bg=color, fg="white",
            activebackground="#ffffff", activeforeground=color, width=18, command=command
        )
        button.pack(side=tk.LEFT, padx=10, pady=5)

    # Menambahkan Listbox untuk menampilkan daftar buku
    listbox_books = tk.Listbox(root, font=font_style, width=100, height=15, bg="#f5f5f5", fg="#333333")
    listbox_books.pack(pady=10)
    listbox_books.bind('<<ListboxSelect>>', update_book)

    # Membuat footer
    footer_frame = tk.Frame(root, bg="#003865")
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    tk.Label(
        footer_frame, text="© 2024 Perpustakaan Digital", 
        font=("Arial", 10), bg="#003865", fg="white", pady=5
    ).pack()

    read_books()  # Menampilkan daftar buku saat aplikasi dijalankan
    root.mainloop()

# Menjalankan aplikasi
if __name__ == "__main__":
    create_gui()
