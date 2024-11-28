import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# Tentukan backend untuk Matplotlib (berguna di lingkungan non-GUI seperti terminal)
import matplotlib
matplotlib.use('TkAgg')  # Gunakan 'TkAgg' jika Anda tidak menggunakan GUI

# Tentukan path ke file CSV
csv_path = "C:/Users/62823/Downloads/archive/Minimum Wage Data.csv"  # Sesuaikan path jika perlu

# Coba baca file CSV dengan penanganan error yang tepat
try:
    # Baca dataset dengan encoding yang berbeda (ISO-8859-1 atau latin1)
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")  # Sesuaikan encoding jika perlu
    print("File berhasil dibaca.")
except FileNotFoundError:
    print(f"File tidak ditemukan di path: {csv_path}")
    exit()  # Keluar dari skrip jika file tidak ditemukan
except Exception as e:
    print(f"Terjadi kesalahan saat membaca file: {e}")
    exit()

# Cek kolom yang tersedia untuk memastikan 'Low.2018' ada
print("Kolom yang tersedia:", df.columns)

# Pastikan kolom 'Low.2018' ada
if 'Low.2018' not in df.columns:
    print("Kolom 'Low.2018' tidak ditemukan. Periksa struktur file.")
    exit()  # Keluar jika kolom tidak ditemukan

# Membuat DataFrame 'act_min_wage' dengan mengelompokkan data berdasarkan negara bagian
act_min_wage = pd.DataFrame()

# Proses data untuk merestrukturisasi berdasarkan negara bagian pada tahun 2018
for name, group in df.groupby("State"):
    if act_min_wage.empty:
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name})
    else:
        act_min_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018": name}))

# Tampilkan beberapa baris pertama dari 'act_min_wage' untuk memverifikasi
print(act_min_wage.head())

# Ganti nilai nol dengan NaN dan hapus kolom yang seluruhnya NaN
min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1).corr()

# Tampilkan beberapa baris pertama dari matriks korelasi
print(min_wage_corr.head())

# Periksa apakah matriks korelasi kosong
if min_wage_corr.empty:
    print("Matriks korelasi kosong. Grafik tidak akan dibuat.")
else:
    # Buat heatmap dari matriks korelasi menggunakan Matplotlib
    plt.matshow(min_wage_corr, cmap=plt.cm.RdYlGn)
    plt.colorbar()  # Tampilkan color bar untuk menunjukkan tingkat korelasi
    plt.title("Heatmap Korelasi Upah Minimum")

    # Sesuaikan label untuk keterbacaan
    labels = [c[:2] for c in min_wage_corr.columns]  # Singkat nama negara bagian untuk label

    # Sesuaikan ukuran grafik dan atur label untuk sumbu x dan y
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)  # Buat sumbu untuk heatmap
    ax.matshow(min_wage_corr, cmap=plt.cm.RdYlGn)  # Tampilkan matriks

    ax.set_xticks(np.arange(len(labels)))  # Tampilkan label untuk sumbu x
    ax.set_yticks(np.arange(len(labels)))  # Tampilkan label untuk sumbu y
    ax.set_xticklabels(labels)  # Atur label sumbu x menjadi singkatan negara bagian
    ax.set_yticklabels(labels)  # Atur label sumbu y menjadi singkatan negara bagian

    plt.show()  # Tampilkan grafik
