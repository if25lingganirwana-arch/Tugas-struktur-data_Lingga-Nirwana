
import csv
from collections import deque

CSV_FILE = "perpustakaan.csv"

FIELDNAMES = [
    "id_buku","judul","penulis","tahun","status","peminjam","waiting_list"
]

def init_csv():
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_data():
    data = []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def save_data(data):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

def find_book(data, book_id):
    for b in data:
        if b["id_buku"] == book_id:
            return b
    return None

def tambah_buku():
    data = load_data()
    data.append({
        "id_buku": input("ID Buku: "),
        "judul": input("Judul: "),
        "penulis": input("Penulis: "),
        "tahun": input("Tahun: "),
        "status": "Tersedia",
        "peminjam": "",
        "waiting_list": ""
    })
    save_data(data)
    print("Buku berhasil ditambahkan.")

def lihat_buku():
    for b in load_data():
        print(f'{b["id_buku"]} | {b["judul"]} | {b["penulis"]} | {b["tahun"]} | {b["status"]}')

def edit_buku():
    data = load_data()
    bid = input("ID Buku: ")
    buku = find_book(data, bid)
    if buku:
        buku["judul"] = input("Judul baru: ")
        buku["penulis"] = input("Penulis baru: ")
        buku["tahun"] = input("Tahun baru: ")
        save_data(data)
        print("Data diperbarui.")
    else:
        print("Buku tidak ditemukan.")

def hapus_buku():
    data = load_data()
    bid = input("ID Buku: ")
    data = [b for b in data if b["id_buku"] != bid]
    save_data(data)
    print("Data dihapus.")

def pinjam_buku():
    data = load_data()
    bid = input("ID Buku: ")
    nama = input("Nama Peminjam: ")
    buku = find_book(data, bid)

    if not buku:
        print("Buku tidak ditemukan.")
        return

    if buku["status"] == "Tersedia":
        buku["status"] = "Dipinjam"
        buku["peminjam"] = nama
        print("Buku berhasil dipinjam.")
    else:
        q = deque(buku["waiting_list"].split("|")) if buku["waiting_list"] else deque()
        q.append(nama)
        buku["waiting_list"] = "|".join(q)
        print("Buku sedang dipinjam. Masuk waiting list.")

    save_data(data)

def kembalikan_buku():
    data = load_data()
    bid = input("ID Buku: ")
    buku = find_book(data, bid)

    if not buku:
        print("Buku tidak ditemukan.")
        return

    q = deque(buku["waiting_list"].split("|")) if buku["waiting_list"] else deque()

    if q:
        next_user = q.popleft()
        buku["peminjam"] = next_user
        buku["waiting_list"] = "|".join(q)
        buku["status"] = "Dipinjam"
        print(f"Buku otomatis diberikan ke: {next_user}")
    else:
        buku["status"] = "Tersedia"
        buku["peminjam"] = ""

    save_data(data)

def cari_buku():
    keyword = input("Masukkan judul: ").lower()
    for b in load_data():
        if keyword in b["judul"].lower():
            print(b)

def sort_buku():
    data = sorted(load_data(), key=lambda x: x["judul"].lower())
    for b in data:
        print(f'{b["id_buku"]} | {b["judul"]}')

def menu():
    init_csv()
    while True:
        print("\n=== SISTEM PERPUSTAKAAN ===")
        print("1. Tambah Buku")
        print("2. Lihat Buku")
        print("3. Edit Buku")
        print("4. Hapus Buku")
        print("5. Pinjam Buku")
        print("6. Kembalikan Buku")
        print("7. Cari Buku")
        print("8. Sort Buku")
        print("9. Keluar")

        pilih = input("Pilih: ")

        if pilih == "1": tambah_buku()
        elif pilih == "2": lihat_buku()
        elif pilih == "3": edit_buku()
        elif pilih == "4": hapus_buku()
        elif pilih == "5": pinjam_buku()
        elif pilih == "6": kembalikan_buku()
        elif pilih == "7": cari_buku()
        elif pilih == "8": sort_buku()
        elif pilih == "9": break
        else: print("Menu tidak valid")

if __name__ == "__main__":
    menu()
